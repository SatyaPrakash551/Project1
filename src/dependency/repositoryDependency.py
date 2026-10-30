from src.db.db_config import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from src.repository.userRepository import UserRepository
def getUserRepository(session:AsyncSession= Depends(get_session)):
    return UserRepository(session)