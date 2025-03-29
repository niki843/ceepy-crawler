import asyncio

from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.screenshot import Screenshots
from app.utils.enums import ScreenshotStatus
from sqlalchemy import insert


class ScreenshotService:
    SCREENSHOT_DIR = "./app/utils/screenshots/"

    @classmethod
    async def start_screenshots(cls, start_url: str , extracted_links: int, db_session: AsyncSession):
        path = cls._generate_path(start_url)
        screenshot = Screenshots(url=start_url, path=path, status=ScreenshotStatus.PENDING.value)
        db_session.add(screenshot)
        await db_session.commit()
        await db_session.refresh(screenshot)

        # Create task to fetch screenshots
        asyncio.create_task(cls.take_screenshot(start_url, extracted_links, path))

        return screenshot.id

    @classmethod
    async def take_screenshot(cls, start_url: str , extracted_links: int, path: str):
        # TODO: implement creating screenshots with playwright
        print(f"Screenshot of: {start_url}, links: {extracted_links}, path:{path}")
        return

    @classmethod
    def _generate_path(cls, url: str):
        path = cls.SCREENSHOT_DIR + url + str(date.today())
        return path

    @classmethod
    async def get_screenshot(id: str):
        # TODO: implement returning screenshots
        print(f"Id: {id}")
        return
