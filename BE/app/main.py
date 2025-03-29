from fastapi import FastAPI

from app.routes import screenshot, health

app = FastAPI(title="Web Crawler API")

@app.get("/")
def read_root():
    return {"message": "Creepy crawler app"}

# Include Routes
app.include_router(screenshot.router)
app.include_router(health.router)