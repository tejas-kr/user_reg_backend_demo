import uvicorn
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI
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

app.include_router(users.router)
app.include_router(books.router)


@app.get('/healthCheck')
def health_check():
    """
    Checks if the site is running.
    :return: Dict. Site Status
    """
    logger.info("HealthCheck Success")
    return {"status": "Site Working"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
