from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base=declarative_base()
engine=create_engine('localhost:5433/auth')
SessionLocal=sessionmaker(autoflush=False,bind=engine)
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
