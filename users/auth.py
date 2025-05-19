from fastapi.security.oauth2 import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from fastapi import APIRouter,Depends, HTTPException,Response
from users.model import Users,get_db
from sqlalchemy.inspection import inspect
from passlib.context import CryptContext
from users.schemas import *
import datetime
import jwt

user_router=APIRouter()
crypt_context=CryptContext(schemes=['bcrypt'],deprecated='auto')
SECRET_KEY = "a_secret_key_for_jwt_token"
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="access_token")

def to_dict(obj):
    return {c.key:getattr(obj,c.key) for c in inspect(obj).mapper.column_attrs}

def create_access_token(data):
    to_encode=data.copy()
    exp=datetime.datetime.now()+datetime.timedelta(minutes=60)
    to_encode['exp']=exp
    token=jwt.encode(to_encode,SECRET_KEY,[ALGORITHM])
    return token

@user_router.get('/user')
def get_user(id:int,db=Depends(get_db))->dict:
    try:
        user=db.query(Users).where(Users.id==id).one()
        if not user:
            raise HTTPException(status_code=404,detail="No user found")
        db.close()
        return {'user':to_dict(user)}
    except:
            raise HTTPException(status_code=500,detail="Something went wrong")
        
@user_router.post('/token')
def auth_user(user:UserAuth,db=Depends(get_db),response=Response)->dict:
    try:
        db_user=db.query(Users).where(Users.email==user.email).one()
        if not user:
            raise HTTPException(status_code=404,detail="Email not registered")
        verified=crypt_context.verify(user.password,db_user.password)
        if verified:
            token=create_access_token(to_dict(user))
            
            response.set_cookie(key='access_token',value=token,expires=datetime.timedelta(minutes=60),httponly=True,secure=True)
            
            db.close()
            return {'user':to_dict(user)}
            
    except:
            raise HTTPException(status_code=500,detail="Something went wrong")
        
@user_router.get('/users/me')
def get_current_user(token:str=Depends(oauth2_scheme)):
    try:
        user=jwt.decode(token,SECRET_KEY,[ALGORITHM])
        if not user.email:
            raise HTTPException(status_code=404,detail="User not logged in properly")
        return user
                
    except:
        raise HTTPException(status_code=500,detail="JWT Exception")
    
@user_router.post('/register')
def register_user(new_user:UserRegister,db=Depends(get_db))->dict:
    try:
        user_present=db.query(Users).where(Users.email==new_user.email).one()
        if user_present:
            raise HTTPException(status_code=409,detail="user already present")
        hashed_pw=crypt_context.hash(new_user.password)
        new_user={
            'email':new_user.email,
            'password':hashed_pw,
            'name':new_user.name
        }
        user_obj=Users(**new_user)
        db.add(user_obj)
        db.commit()
        db.close()
        return {'detail':'User added successfully','user':new_user}
    except:
        raise HTTPException(status_code=500,detail="Cannot add the user")
    
@user_router.patch('/change_pw')
def change_password(user:PasswordChange,db=Depends(get_db))->dict:
    try:
        cur_user=db.query(Users).where(Users.id==user.id).one()
        if not cur_user:
            raise HTTPException(status_code=404,detail="user not present")
            
        cur_user.password=crypt_context.hash(user.password)
        db.commit()
        db.close()
        return {'status':True,'detail':'Password Changed Successfully'}
    except:
        raise HTTPException(status_code=500,detail="Cannot add the user")
        
        
        
        
        
        
        
    

            
            
            
        
        
             
        
    