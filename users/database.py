from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base=declarative_base()
engine = create_engine('postgresql://postgres:password@localhost:5433/test')
SessionLocal=sessionmaker(autoflush=False,bind=engine)
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
