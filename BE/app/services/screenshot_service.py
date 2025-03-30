import asyncio
import os

from datetime import datetime
from venv import logger

from playwright.async_api import async_playwright
from sqlalchemy import select, update, desc
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import FileResponse

from app.models.screenshot import Screenshot
from app.utils.core import fetch_file_names_in_path, get_host_from_url, sanitize_str
from app.utils.enums import ScreenshotStatus


class ScreenshotService:
    SCREENSHOT_DIR = "./app/utils/screenshots/"

    @classmethod
    async def start_screenshots(
        cls, start_url: str, extracted_links: int, db_session: AsyncSession
    ):
        screenshots = await db_session.execute(
            select(Screenshot)
            .filter(Screenshot.url == start_url)
            .order_by(desc(Screenshot.created_at))
            .limit(1)
        )
        screenshot = screenshots.scalars().first()

        # Validate if the screenshots were created today, having in mind that they might be changed if they are older
        # Check if there are enough screenshots depending on the required + 1 because of the start link
        if (
            screenshot.created_at.date() == datetime.now().date()
            and len(fetch_file_names_in_path(screenshot.path)) <= extracted_links + 1
        ):
            return screenshot.id

        created_at = datetime.now()
        path = cls._generate_path(start_url, str(created_at))
        screenshot = Screenshot(
            url=start_url,
            path=path,
            status=ScreenshotStatus.PENDING.value,
            created_at=created_at,
        )
        db_session.add(screenshot)
        await db_session.commit()
        await db_session.refresh(screenshot)

        # Create task to fetch screenshots
        asyncio.create_task(
            cls.take_screenshot(
                start_url, extracted_links, path, db_session, str(screenshot.id)
            )
        )

        return screenshot.id

    @classmethod
    async def take_screenshot(
        cls,
        start_url: str,
        extracted_links: int,
        path: str,
        db_session: AsyncSession,
        id: str,
    ):
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch()
            page = await browser.new_page()
            await page.goto(start_url)

            file_name = f"{get_host_from_url(start_url)}.png"
            await page.screenshot(path=path + file_name, type="png")

            # Fetch all links
            links = await page.locator("a").evaluate_all(
                "elements => elements.map(el => el.href)"
            )

            # Remove duplicates and invalid urls
            links = list(set(links))
            links.remove("")

            # Follow and screenshot extracted_links count
            for index in range(0, extracted_links):
                if index >= len(links):
                    break

                if links[index] == start_url:
                    continue

                try:
                    await page.goto(links[index])
                except Exception as e:
                    logger.error(f"Failed to load link: {links[index]} Error: {e}")
                    continue

                file_name = f"{get_host_from_url(links[index])}{index}.png"
                await page.screenshot(path=path + file_name, type="png")

            await browser.close()

        await db_session.execute(
            update(Screenshot)
            .where(Screenshot.id == id)
            .values(status=ScreenshotStatus.DONE.value)
        )
        await db_session.commit()

    @classmethod
    def _generate_path(cls, url: str, created_at: str):
        path = (
            cls.SCREENSHOT_DIR
            + get_host_from_url(url)
            + sanitize_str(created_at, "_")
            + "/"
        )
        return path

    @classmethod
    async def get_screenshot(cls, screenshot_id: str, db_session: AsyncSession):
        screenshots = await db_session.execute(
            select(Screenshot).filter(Screenshot.id == screenshot_id)
        )
        screenshot = screenshots.scalars().first()

        if screenshot.status != ScreenshotStatus.DONE.value:
            return {"id": screenshot.id, "status": screenshot.status}

        files = []
        for file in fetch_file_names_in_path(screenshot.path):
            filename = os.fsdecode(file)
            files.append(
                FileResponse(screenshot.path + filename, media_type="image/png")
            )

        return files
