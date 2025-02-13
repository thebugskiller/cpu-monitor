from datetime import datetime
from beanie import Document


class TestRun(Document):
    name: str
    started_at: datetime = datetime.utcnow()

    class Settings:
        collection = "test_runs"
