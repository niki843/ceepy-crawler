from typing import Annotated

from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db_session

DBSessionDep = Annotated[AsyncSession, Depends(get_db_session)]