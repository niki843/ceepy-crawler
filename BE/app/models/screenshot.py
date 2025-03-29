import uuid

from sqlmodel import SQLModel, Field


class Screenshots(SQLModel, table=True):
    id: uuid.UUID | None = Field(default_factory=uuid.uuid4, primary_key=True)
    url: str = Field(nullable=False, index=True)
    path: str = Field(nullable=False)
