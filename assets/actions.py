from database import get_db
from model import Asset, AssetImage
from fastapi import APIRouter, HTTPException, Depends, UploadFile, Response
from pydantic import BaseModel
from typing import List

class CreateAssetBase(BaseModel):
    name:str
    location:str
    price:str
    negotiable:bool

class CreateAssetComp(CreateAssetBase):
    images=List[UploadFile]

crud_router=APIRouter()

@crud_router.post('/create_asset')
def create_asset(asset:CreateAssetComp,db=Depends(get_db)):
    try:
        new_asset=Asset(**asset.model_dump())
        db.add(new_asset)
        db.flush()
        
        for image in asset.images:
            imdata=image.file.read()
            new_imdata=AssetImage(asset_id=new_asset.id,image=imdata)
            db.add(new_imdata)
            db.flush()
        db.commit()
        db.close()
    except Exception as e:
        print(e)
        
@crud_router.get('/{id}')
def get_asset_by_id(id:int,db=Depends(get_db)):
    asset=db.query(Asset).where(Asset.id==id)
    asset_dict=asset.model_dump()
    asset_imgs=db.query(AssetImage).where(AssetImage.asset_id==id).all()
    imgs=[]
    for img in asset_imgs:
        imgs.append(img.id)
    asset_dict['imgs']=imgs
    
@crud_router.get('/image/{id}')
def get_image_by_id(id:int,db=Depends(get_db)):
    image=db.query(AssetImage.image).where(AssetImage.id==id).scalar()
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")

    return Response(content=image.data, media_type=image.content_type or "application/octet-stream")
    