from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import Integer,String
from src.db.db_config import Base


class User(Base):
    __tablename__ = "user"
    user_id: Mapped[int]= mapped_column(Integer,primary_key=True,autoincrement=True)
    email : Mapped[str] = mapped_column(String(100),nullable=False, unique=True)
    password : Mapped[str] = mapped_column(String(100),nullable=False)