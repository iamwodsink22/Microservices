from sqlalchemy import Integer,Float,String,ARRAY,Column,DateTime,func,Boolean,ForeignKey,LargeBinary
from sqlalchemy.orm import relationship
from database import Base,engine

class BaseMixin(Base):
    id=Column(Integer,autoincrement=True,primary_key=True)
    created_at=Column(DateTime(timezone=True),server_default=func.now())
    
    
class AssetImage(Base,BaseMixin):
    __tablename__='assetimage'
    asset_id=Column(Integer,ForeignKey("Asset.id"))
    image=Column(LargeBinary,nullable=False)
    asset=relationship("Asset",back_populates="images")
    
class Asset(Base,BaseMixin):
    __tablename__="asset"
    name=Column(String,nullable=False)
    location=Column(String,nullable=False)
    price=Column(Float,nullable=False)
    negotiable=Column(Boolean,nullable=False)
    user_id=Column(Integer,nullable=False)
    images=relationship("AssetImage",back_populates="asset")
    
Base.metadata.create_all(engine)
    

    
    
    