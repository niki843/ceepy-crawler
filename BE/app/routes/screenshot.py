from fastapi import APIRouter

from app.schemas.screenshot import ScreenshotDTO
from app.services.screenshot_service import ScreenshotService
from app.dependencies.core import DBSessionDep

router = APIRouter()

@router.post("/screenshot")
async def capture_screenshot(screenshot_dto: ScreenshotDTO, db_session: DBSessionDep):
    """Captures a screenshot of the given URL."""
    screenshot_id = await ScreenshotService.start_screenshots(screenshot_dto.start_url, screenshot_dto.extracted_links, db_session)
    return {"screenshot_id": screenshot_id}

@router.get("/screenshot/{id}")
async def fetch_screenshot(id: str, db_session: DBSessionDep):
    """Retrieves a screenshot from storage."""
    return await ScreenshotService.get_screenshot(id, db_session)
