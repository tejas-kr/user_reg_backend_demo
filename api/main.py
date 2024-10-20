import os
import uvicorn
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel
from .utils.log_util import logger
from .utils.db_utils import engine
from .auth import users
from .books import books


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    logger.info("Create SQLite DB File")
    SQLModel.metadata.create_all(engine)

    yield  # The yield pauses the function while the application runs

    logger.info("Shutting down")


app = FastAPI(lifespan=lifespan)

origins: list = os.getenv("CROSS_ORIGINS", "").split(';')
logger.info(f"ORIGINS: {origins}")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of allowed origins
    allow_credentials=True,  # Allow cookies to be sent cross-origin
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all custom headers
)

app.include_router(users.router)
app.include_router(books.router)


@app.get('/healthCheck')
async def health_check():
    """
    Checks if the site is running.
    :return: Dict. Site Status
    """
    logger.info("HealthCheck Success")
    return {"status": "Site Working"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
