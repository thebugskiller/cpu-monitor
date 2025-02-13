from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from src.models import User, TestRun
from config.settings import config

client = AsyncIOMotorClient(config.MONGO_URI)
db = client[config.DB_NAME]

async def init_db():
    await init_beanie(database=db, document_models=[User, TestRun])
