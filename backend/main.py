from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import httpx
from typing import Dict, Any
import os
from dotenv import load_dotenv
import asyncio
from datetime import datetime
from database import save_power_data, get_latest_power_data, get_all_power_data
from config import settings

load_dotenv()


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# Background task flag and token storage
background_task_running = False
current_token = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler for startup and shutdown"""
    global background_task_running

    # Startup
    print("=" * 60)
    print(f"{bcolors.HEADER}{bcolors.BOLD}Starting API Map Backend...{bcolors.ENDC}")
    print("=" * 60)

    # Get initial token
    print(f"\n{bcolors.OKBLUE}1. Obtaining initial token...{bcolors.ENDC}")
    await renew_token()

    if current_token:
        print(f"{bcolors.OKGREEN}[SUCCESS] Initial token obtained successfully{bcolors.ENDC}")
    else:
        print(f"{bcolors.FAIL}[ERROR] Failed to obtain initial token{bcolors.ENDC}")
        print(f"{bcolors.WARNING}[WARNING] API calls will fail until token is obtained!{bcolors.ENDC}")

    # Start background data collection
    print(f"\n{bcolors.OKBLUE}2. Starting background data collection task...{bcolors.ENDC}")
    data_task = asyncio.create_task(collect_data_periodically())

    # Start background token renewal (every 23h59min)
    print(f"\n{bcolors.OKBLUE}3. Starting background token renewal task...{bcolors.ENDC}")
    token_task = asyncio.create_task(renew_token_periodically())

    print("\n" + "=" * 60)
    print(f"{bcolors.OKGREEN}{bcolors.BOLD}[SUCCESS] Backend initialization complete!{bcolors.ENDC}")
    print("=" * 60 + "\n")

    yield  # Application runs here

    # Shutdown
    background_task_running = False
    print(f"{bcolors.WARNING}[SHUTDOWN] Background data collection stopped{bcolors.ENDC}")

    # Cancel background tasks
    data_task.cancel()
    token_task.cancel()

    # Wait for tasks to complete cancellation
    try:
        await data_task
    except asyncio.CancelledError:
        # Task was cancelled during shutdown; this is expected and can be safely ignored.
        pass

    try:
        await token_task
    except asyncio.CancelledError:
        # Task was cancelled during shutdown; this is expected and can be safely ignored.
        pass


app = FastAPI(title="API Map Backend", lifespan=lifespan)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,  # Use settings from .env file
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def renew_token():
    """Renews token and updates the global current_token"""
    global current_token

    url = "https://gateway.isolarcloud.com.hk/openapi/login"
    headers = {
        "Content-Type": "application/json",
        "x-access-key": os.getenv("API_ACCESS_KEY", None),
        "sys_code": "901"
    }
    data = {
        "appkey": os.getenv("API_APPKEY", None),
        "user_account": os.getenv("USER_ACCOUNT", None),
        "user_password": os.getenv("USER_PASSWORD", None),
    }

    if (not headers.get("x-access-key") or
            not data.get("appkey") or
            not data.get("user_account") or
            not data.get("user_password")
    ):
        print(f"{bcolors.FAIL}[ERROR] Missing credentials in .env file for token renewal{bcolors.ENDC}")
        return None

    print(f"{bcolors.OKCYAN}-> Attempting to renew token...{bcolors.ENDC}")

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            login_response = await client.post(url, json=data, headers=headers)
            login_response.raise_for_status()
            response_data = login_response.json()

            print(f"   Response Code: {response_data.get('result_code')}")
            print(f"   Response Msg: {response_data.get('result_msg', 'N/A')}")

            if response_data.get("result_code") == "1":
                token_found = None

                # Location 1: result_data.token
                if 'result_data' in response_data and isinstance(response_data['result_data'], dict):
                    token_found = response_data['result_data'].get('token')
                    if token_found:
                        print(f"   Token found in: result_data.token")

                # Location 2: direct token field
                if not token_found and 'token' in response_data:
                    token_found = response_data.get('token')
                    if token_found:
                        print(f"   Token found in: token")

                # Location 3: result_data as string (might be the token itself)
                if not token_found and 'result_data' in response_data and isinstance(response_data['result_data'], str):
                    token_found = response_data['result_data']
                    if token_found:
                        print(f"   Token found in: result_data (string)")

                if token_found:
                    current_token = token_found
                    print(
                        f"{bcolors.OKGREEN}[SUCCESS] Token renewed successfully at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{bcolors.ENDC}")
                    print(f"   Token: {current_token[:20]}... (truncated, length: {len(current_token)})")
                    return current_token
                else:
                    print(f"{bcolors.FAIL}[ERROR] Token renewal failed: Token is empty in response{bcolors.ENDC}")
                    print(f"   Full response keys: {list(response_data.keys())}")
                    print(f"   Full response: {response_data}")
                    return None
            else:
                print(
                    f"{bcolors.FAIL}[ERROR] Token renewal failed: {response_data.get('result_msg', 'Unknown error')}{bcolors.ENDC}")
                print(f"   Full response: {response_data}")
                return None
        except httpx.HTTPError as e:
            print(f"{bcolors.FAIL}[ERROR] HTTP error during token renewal: {e}{bcolors.ENDC}")
            return None
        except Exception as e:
            print(f"{bcolors.FAIL}[ERROR] Unexpected error during token renewal: {e}{bcolors.ENDC}")
            import traceback
            traceback.print_exc()
            return None


async def fetch_power_data_from_api() -> Dict[str, Any]:
    """
    Internal function to fetch power station data from the external API
    Uses the global current_token and renews it if invalid
    """
    global current_token

    # If no token, get one first
    if not current_token:
        print(f"{bcolors.WARNING}[WARNING] No token available, attempting to renew...{bcolors.ENDC}")
        await renew_token()

    # Ensure we have a token before making the request
    if not current_token:
        error_msg = "Failed to obtain token - check credentials in .env file"
        print(f"{bcolors.FAIL}[ERROR] {error_msg}{bcolors.ENDC}")
        return {"error": error_msg, "result_code": "0"}

    url = "https://gateway.isolarcloud.com.hk/openapi/getPowerStationInfoPowerByCodeList"
    headers = {
        "Content-Type": "application/json",
        "x-access-key": os.getenv("API_ACCESS_KEY"),
        "sys_code": "901"
    }
    data = {
        "token": current_token,  # Use the global token instead of env variable
        "appkey": os.getenv("API_APPKEY"),
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.post(url, json=data, headers=headers)
            response.raise_for_status()
            response_data = response.json()

            # Check if token is invalid and renew if needed
            if response_data.get("result_code") == "E00003" or response_data.get(
                    "result_msg") == "er_token_login_invalid":
                print(f"{bcolors.WARNING}[WARNING] Token invalid, renewing...{bcolors.ENDC}")
                await renew_token()

                # Ensure renewal was successful
                if not current_token:
                    return {"error": "Failed to renew token", "result_code": "0"}

                # Retry with new token
                data["token"] = current_token
                response = await client.post(url, json=data, headers=headers)
                response.raise_for_status()
                response_data = response.json()

            return response_data
        except httpx.HTTPError as e:
            print(f"{bcolors.FAIL}[ERROR] HTTP error in fetch_power_data_from_api: {e}{bcolors.ENDC}")
            return {"error": str(e), "result_code": "0"}
        except Exception as e:
            print(f"{bcolors.FAIL}[ERROR] Unexpected error in fetch_power_data_from_api: {e}{bcolors.ENDC}")
            return {"error": str(e), "result_code": "0"}


async def collect_data_periodically():
    """
    Background task that collects data every 5 minutes and saves to database
    """
    global background_task_running
    background_task_running = True

    print(f"{bcolors.OKBLUE}Background data collection started - fetching every 5 minutes{bcolors.ENDC}")

    while background_task_running:
        try:
            print(
                f"{bcolors.OKCYAN}[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] -> Fetching power data from API...{bcolors.ENDC}")
            data = await fetch_power_data_from_api()

            # Save to database
            record = save_power_data(data)
            print(f"{bcolors.OKGREEN}[SUCCESS] Data saved to database with ID: {record.id}{bcolors.ENDC}")

        except Exception as e:
            print(f"{bcolors.FAIL}[ERROR] Error collecting data: {e}{bcolors.ENDC}")

        # Wait 5 minutes (300 seconds)
        await asyncio.sleep(300)


async def renew_token_periodically():
    """
    Background task that renews the token every 23h59min (86340 seconds)
    """
    global background_task_running

    print(f"{bcolors.OKBLUE}Token renewal task started - renewing every 23h59min{bcolors.ENDC}")

    while background_task_running:
        # Wait 23h59min before next renewal
        await asyncio.sleep(86340)

        if background_task_running:
            print(
                f"{bcolors.OKCYAN}[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] -> Scheduled token renewal...{bcolors.ENDC}")
            await renew_token()


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "API Map Backend is running"}


@app.get("/api/power-data")
async def get_power_data() -> Dict[str, Any]:
    """
    Get the latest power station data from the database
    This endpoint returns the most recent data collected by the background task
    """
    latest_data = get_latest_power_data()

    if latest_data:
        return latest_data
    else:
        return {
            "message": "No data available yet. Background collection is running.",
            "result_code": "0"
        }


@app.get("/api/power-data/history")
async def get_power_data_history(limit: int = 100) -> Dict[str, Any]:
    """
    Get historical power station data from the database
    Query parameter 'limit' controls how many records to return (default: 100)
    """
    history = get_all_power_data(limit=limit)

    return {
        "count": len(history),
        "data": history
    }


@app.get("/api/power-data/fetch-now")
async def fetch_power_data_now() -> Dict[str, Any]:
    """
    Manually trigger a data fetch from the external API and save to database
    Useful for testing or forcing an immediate update
    """
    try:
        data = await fetch_power_data_from_api()
        record = save_power_data(data)

        return {
            "message": "Data fetched and saved successfully",
            "record_id": record.id,
            "timestamp": record.timestamp.isoformat(),
            "data": data
        }
    except Exception as e:
        return {
            "error": str(e),
            "result_code": "0"
        }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "background_task_running": background_task_running
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
