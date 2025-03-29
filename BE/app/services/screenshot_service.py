class ScreenshotService:
    SCREENSHOT_DIR = "./app/utils/screenshots"

    @staticmethod
    async def take_screenshot(start_url:str , extracted_links: int):
        # TODO: implement creating screenshots with playwright
        print(f"Screenshot of: {start_url}, links: {extracted_links}")
        return

    @staticmethod
    async def get_screenshot(id: str):
        # TODO: implement returning screenshots
        print(f"Id: {id}")
        return
