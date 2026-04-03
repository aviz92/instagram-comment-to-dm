from contextlib import asynccontextmanager

from fastapi import FastAPI
from custom_python_logger import get_logger

from app import db
from app.routers import health, webhooks

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up — initializing DB")
    db.init_db()
    yield
    logger.info("Shutting down")


app = FastAPI(
    title="Instagram Comment Trigger",
    description="Sends a private DM when a user comments a keyword on an Instagram post.",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(health.router)
app.include_router(webhooks.router)
