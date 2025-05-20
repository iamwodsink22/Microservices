from database import get_db,Base
from sqlalchemy import Column,Integer,DateTime,func, String,text,Boolean
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
    role_id=Column(int,nullable=False,default=1,server_default=text("1"))
    is_superadmin=Column(Boolean,defaukt=False,server_default=text("false"))
    
    