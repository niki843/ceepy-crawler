from pydantic import BaseModel

# Request Model: Used for creating a screenshot entry
class ScreenshotCreate(BaseModel):
    start_url: str
    extracted_links: int
