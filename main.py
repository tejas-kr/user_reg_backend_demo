from fastapi import FastAPI
from .utils.log_util import logger
from .auth import users
from .books import books

app = FastAPI()

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

