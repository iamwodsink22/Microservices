from fastapi import APIRouter

router = APIRouter()

@router.get("/management/{portal_id}")
def access_portal(portal_id:int): 
    return {'message': 'Services'}