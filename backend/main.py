from fastapi import FastAPI

from db.connector import init_db
from src.api.v1.user import auth_router
from src.api.v1.monitor import monitor_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(monitor_router)


@app.on_event("startup")
async def startup_event():
    await init_db()
