from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv
import os

load_dotenv()

DB_URl = os.getenv("DB_URL")

engine = create_async_engine(DB_URl,echo=True)

sessionLocal = async_sessionmaker(bind=engine,expire_on_commit=False)

class Base(DeclarativeBase):
    pass

async def get_session():
    async with sessionLocal.begin() as session:
        yield session