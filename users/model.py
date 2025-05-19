from database import get_db,Base
from sqlalchemy import Column,Integer,DateTime,func, String
from sqlalchemy.orm import declarative_mixin

@declarative_mixin
class BaseMixin(Base):
    id=Column(Integer,primary_key=True,autoincrement=True)
    created_at=Column(DateTime(timezone=True),server_default=func.now())
    
    
class Users(BaseMixin,Base):
    __tablename__='users'
    name=Column(String(20),nullable=True)
    email=Column(String(20),nullable=False)
    password=Column(String,nullable=False)
    
    