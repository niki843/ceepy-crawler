import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String

from app.database import Base


class Screenshot(Base):
    __tablename__ = "screenshot"

    id:uuid.uuid4 = Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    url: str = Column("url", String(512), nullable=False)
    path: str = Column("path", String(512),nullable=False)
    status: str = Column("status", String(50),nullable=False)
