from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PowerStationData(BaseModel):
    """Model for power station data"""
    code: str
    state_realtime_power: float
    state_installed_power: float


class StateInfo(BaseModel):
    """Model for state information"""
    name: str
    code: str
    active_power: float
    installed_power: float
    utilization: float
    last_updated: Optional[datetime] = None


class APIResponse(BaseModel):
    """Model for API response"""
    result_code: str
    result_msg: Optional[str] = None
    result_data: Optional[list] = None
