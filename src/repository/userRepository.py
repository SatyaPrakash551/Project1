from src.db.db_config import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from src.model.userModel import User
from sqlalchemy import select
class UserRepository:
    def __init__(self,session :AsyncSession ):
        self.session = session

    async def createUser(self, user: User):
        self.session.add(user)
        await self.session.flush()
        await self.session.refresh(user)
        return user

    async def getUser(self, email:str ):
        stmt = select(User).where(User.email == email)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
        # return {"error":"user not found"}