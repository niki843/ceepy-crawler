from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import sessionmanager
from app.routes import screenshot, health

app = FastAPI(title="Web Crawler API")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Function that handles startup and shutdown events.
    To understand more, read https://fastapi.tiangolo.com/advanced/events/
    """
    yield
    if sessionmanager._engine is not None:
        # Close the DB connection
        await sessionmanager.close()

@app.get("/")
def read_root():
    return {"message": "Creepy crawler app"}

# Include Routes
app.include_router(screenshot.router)
app.include_router(health.router)