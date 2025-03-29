import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String

from database import Base


class Screenshots(Base):
    __tablename__ = "screenshots"

    id:uuid.uuid4 = Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    url: str = Column("url", String(512), nullable=False)
    path: str = Column("path", String(512),nullable=False)
