from fastapi import APIRouter

from app.schemas.screenshot import ScreenshotDTO
from app.services.screenshot_service import ScreenshotService

router = APIRouter()

@router.post("/screenshot")
async def capture_screenshot(screenshot_dto: ScreenshotDTO):
    """Captures a screenshot of the given URL."""
    await ScreenshotService.take_screenshot(screenshot_dto.start_url, screenshot_dto.extracted_links)



@router.get("/screenshot/{id}")
async def fetch_screenshot(id: str):
    """Retrieves a screenshot from storage."""
    await ScreenshotService.get_screenshot(id)
    return