from fastapi import APIRouter, HTTPException, Depends
from itsdangerous import URLSafeSerializer

from config.settings import config
from src.models import TestRun, CPUUsage
from src.schema import CPUUsageRequest, BaseTestRun
from src.middleware.auth import get_current_user

serializer = URLSafeSerializer(config.SECRET_KEY)
monitor_router = APIRouter(prefix="/monitor", tags=["Authentication"])


@monitor_router.post("/test-runs")
async def create_test_run(
    test_run: BaseTestRun, user_id: str = Depends(get_current_user)
):
    """Creates a new test run."""
    new_test_run = TestRun(name=test_run.name, started_at=test_run.started_at)
    await new_test_run.insert()
    return {"test_run_id": str(new_test_run.id)}


@monitor_router.post("/cpu-usage/{test_run_id}")
async def log_cpu_usage(
    test_run_id: str, data: CPUUsageRequest, user_id: str = Depends(get_current_user)
):
    """Logs CPU usage for a test run."""
    test_run = await TestRun.get(test_run_id)
    if not test_run:
        raise HTTPException(status_code=404, detail="Test run not found")

    cpu_usage_record = CPUUsage(
        test_run_id=test_run_id, cpu_percent=data.cpu_percent, timestamp=data.timestamp
    )

    await CPUUsage.insert(cpu_usage_record)

    return {"message": "CPU usage recorded"}


@monitor_router.get("/cpu-usage/{test_run_id}")
async def get_cpu_usage(test_run_id: str, user_id: str = Depends(get_current_user)):
    """Retrieves all CPU usage logs for a test run."""
    test_run = await TestRun.get(test_run_id)
    if not test_run:
        raise HTTPException(status_code=404, detail="Test run not found")

    usage_logs = await CPUUsage.find(CPUUsage.test_run_id == test_run_id).to_list()
    logs = [
        {"timestamp": log.timestamp, "cpu_percent": log.cpu_percent}
        for log in usage_logs
    ]
    return {"name": test_run.name, "started_at": test_run.started_at, "cpu_usage": logs}
