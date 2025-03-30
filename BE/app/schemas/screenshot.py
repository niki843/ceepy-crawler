from pydantic import BaseModel, HttpUrl


# Request Model: Used for creating a screenshot entry
class ScreenshotDTO(BaseModel):
    start_url: HttpUrl
    extracted_links: int
