from pydantic import BaseModel, Field
from datetime import datetime


class BaseTestRun(BaseModel):
    name: str = Field(..., min_length=3, description="Name (min 6 characters)")
    started_at: datetime = Field(..., description="Timestamp when the test started")


class NamedTestRun(BaseTestRun):
    id: str


class CPUUsageRequest(BaseModel):
    cpu_percent: float = Field(..., ge=0, le=100, description="CPU usage percentage (0-100%)")
    timestamp: datetime = Field(..., description="Timestamp when the test started")
