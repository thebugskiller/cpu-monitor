from datetime import datetime
from beanie import Document


class CPUUsage(Document):
    test_run_id: str
    timestamp: datetime = datetime.utcnow()
    cpu_percent: float

    class Settings:
        collection = "cpu_usage"
