from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import httpx
from typing import Dict, Any
import os
from dotenv import load_dotenv

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


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "API Map Backend is running"}


@app.get("/api/power-data")
async def get_power_data() -> Dict[str, Any]:
    """
    Fetch power station data from the external API
    This endpoint acts as a proxy to avoid CORS issues and centralize API calls
    """
    url = "https://gateway.isolarcloud.com.hk/openapi/getPowerStationInfoPowerByCodeList"
    headers = {
        "Content-Type": "application/json",
        "x-access-key": os.getenv("API_ACCESS_KEY", "3g1nrc7c59kxygt2i7idana49jpvw01f"),
        "sys_code": os.getenv("API_SYS_CODE", "901")
    }
    data = {
        "token": os.getenv("API_TOKEN", "110295_b1f25dda84f640c7acc6456bbbec9a47"),
        "appkey": os.getenv("API_APPKEY", "664780B4B466AB6F19DF393D5055D977")
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=data, headers=headers)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            return {"error": str(e), "result_code": "0"}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
