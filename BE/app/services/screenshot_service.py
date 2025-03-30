import asyncio
import os

from datetime import datetime
from pathlib import Path
from venv import logger

from fastapi import HTTPException
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
        # Order by request links and created at to ensure getting the newest record with the maximum files
        screenshots = await db_session.execute(
            select(Screenshot)
            .filter(Screenshot.url == start_url)
            .order_by(desc(Screenshot.requested_links), desc(Screenshot.created_at))
            .limit(1)
        )
        screenshot = screenshots.scalars().first()

        # Validate if the screenshots were created today, having in mind that they might be changed if they are older
        # Check if there are enough screenshots depending on the required + 1 because of the start link
        # Return new record using the already created path
        if (
            screenshot
            and screenshot.created_at.date() == datetime.now().date()
            and screenshot.requested_links >= extracted_links
        ):
            new_screenshot = Screenshot(
                url=start_url,
                path=screenshot.path,
                status=ScreenshotStatus.DONE.value,
                requested_links=extracted_links,
                created_at=datetime.now(),
            )
            db_session.add(new_screenshot)
            await db_session.commit()
            await db_session.refresh(new_screenshot)

            return new_screenshot.id

        created_at = datetime.now()
        path = cls._generate_path(start_url, str(created_at))
        screenshot = Screenshot(
            url=start_url,
            path=path,
            status=ScreenshotStatus.PENDING.value,
            requested_links=extracted_links,
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

            file_name = f"0{get_host_from_url(start_url)}.png"
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

                # Added indexing as start of file naming to ensure order is kept
                file_name = f"{index+1}{get_host_from_url(links[index])}.png"
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
        print(path)
        return path

    @classmethod
    async def get_screenshots(cls, screenshot_id: str, db_session: AsyncSession, base_url: str):
        screenshots = await db_session.execute(
            select(Screenshot).filter(Screenshot.id == screenshot_id)
        )
        screenshot = screenshots.scalars().first()

        if not screenshot:
            raise HTTPException(status_code=404, detail="Screenshot not found")

        if screenshot.status != ScreenshotStatus.DONE.value:
            return {"id": screenshot.id, "status": screenshot.status}

        full_path = Path(screenshot.path)
        base_path = Path("./app/utils")
        relative_path = str(full_path.relative_to(base_path))

        all_files = fetch_file_names_in_path(screenshot.path)
        response_files = []
        for index in range(0, screenshot.requested_links + 1):
            filename = os.fsdecode(all_files[index])
            response_files.append(
                FileResponse(base_url + relative_path + "/" + filename, media_type="image/png")
            )

        return response_files
