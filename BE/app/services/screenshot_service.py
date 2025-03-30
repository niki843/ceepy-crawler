import asyncio
import os

from datetime import date

from playwright.async_api import async_playwright
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import FileResponse

from app.models.screenshot import Screenshot
from app.utils.enums import ScreenshotStatus


class ScreenshotService:
    SCREENSHOT_DIR = "./app/utils/screenshots/"

    @classmethod
    async def start_screenshots(cls, start_url: str , extracted_links: int, db_session: AsyncSession):
        path = cls._generate_path(start_url)
        screenshot = Screenshot(url=start_url, path=path, status=ScreenshotStatus.PENDING.value)
        db_session.add(screenshot)
        await db_session.commit()
        await db_session.refresh(screenshot)

        # Create task to fetch screenshots
        asyncio.create_task(cls.take_screenshot(start_url, extracted_links, path, db_session, str(screenshot.id)))

        return screenshot.id

    @classmethod
    async def take_screenshot(cls, start_url: str , extracted_links: int, path: str, db_session: AsyncSession, id:str):
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch()
            page = await browser.new_page()
            await page.goto(start_url)
            await page.screenshot(path=path, type="png")
            await browser.close()

        await db_session.execute(update(Screenshot).where(Screenshot.id==id).values(status=ScreenshotStatus.DONE.value))
        await db_session.commit()

    @classmethod
    def _generate_path(cls, url: str):
        path = cls.SCREENSHOT_DIR + url + str(date.today())
        return path

    @classmethod
    async def get_screenshot(cls, screenshot_id: str, db_session: AsyncSession):
        screenshots = await db_session.execute(select(Screenshot).filter(Screenshot.id == screenshot_id))
        screenshot = screenshots.scalars().first()

        if screenshot.status != ScreenshotStatus.DONE.value:
            return {"id": screenshot.id, "status": screenshot.status}

        directory = os.fsencode(screenshot.path)
        files = []
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            files.append(FileResponse(screenshot.path + filename, media_type="image/png"))

        return files
