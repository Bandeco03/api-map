from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import httpx
from typing import Dict, Any
import os
from dotenv import load_dotenv
import asyncio
from datetime import datetime
from database import save_power_data, get_latest_power_data, get_all_power_data

load_dotenv()

app = FastAPI(title="API Map Backend")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Background task flag
background_task_running = False


async def fetch_power_data_from_api() -> Dict[str, Any]:
    """
    Internal function to fetch power station data from the external API
    """
    url = "https://gateway.isolarcloud.com.hk/openapi/getPowerStationInfoPowerByCodeList"
    headers = {
        "Content-Type": "application/json",
        "x-access-key": os.getenv("API_ACCESS_KEY"),
        "sys_code": "901"
    }
    data = {
        "token": os.getenv("API_TOKEN"),
        "appkey": os.getenv("API_APPKEY"),
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=data, headers=headers)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            return {"error": str(e), "result_code": "0"}


async def collect_data_periodically():
    """
    Background task that collects data every 5 minutes and saves to database
    """
    global background_task_running
    background_task_running = True

    print("Background data collection started - fetching every 5 minutes")

    while background_task_running:
        try:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] -> Fetching power data from API...")
            data = await fetch_power_data_from_api()

            # Save to database
            record = save_power_data(data)
            print(f"✅ Data saved to database with ID: {record.id}")

        except Exception as e:
            print(f"❌ Error collecting data: {e}")

        # Wait 5 minutes (300 seconds)
        await asyncio.sleep(300)


@app.on_event("startup")
async def startup_event():
    """Start background task when the application starts"""
    asyncio.create_task(collect_data_periodically())


@app.on_event("shutdown")
async def shutdown_event():
    """Stop background task when the application shuts down"""
    global background_task_running
    background_task_running = False
    print("🛑 Background data collection stopped")


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
    uvicorn.run(app, host="0.0.0.0", port=8000)
