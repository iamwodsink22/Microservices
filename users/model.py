from database import get_db,Base
from sqlalchemy import Column,Integer,DateTime,func, String,text,Boolean
from sqlalchemy.orm import declarative_mixin
from database import Base,engine
@declarative_mixin
class BaseMixin:
    id=Column(Integer,primary_key=True,autoincrement=True)
    created_at=Column(DateTime(timezone=True),server_default=func.now())
    
    
class Users(Base,BaseMixin):
    __tablename__='users'
    name=Column(String(50),nullable=True)
    email=Column(String(50),nullable=False)
    phone=Column(Integer,nullable=False)
    password=Column(String,nullable=False)
    role_id=Column(Integer,nullable=False,default=1,server_default=text("1"))
    is_superadmin=Column(Boolean,default=False,server_default=text("false"))
    
Base.metadata.create_all(engine)

    
    