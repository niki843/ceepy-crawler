from fastapi import APIRouter

from app.schemas.screenshot import ScreenshotCreate

router = APIRouter()

@router.post("/screenshot")
async def capture_screenshot(screenshot_create: ScreenshotCreate):
    """Captures a screenshot of the given URL."""
    pass

@router.get("/screenshot/{filename}")
async def fetch_screenshot(filename: str):
    """Retrieves a screenshot from storage."""
    pass