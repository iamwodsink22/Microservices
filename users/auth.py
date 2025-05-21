from fastapi.security.oauth2 import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from fastapi import APIRouter,Depends, HTTPException,Response, Request
from model import Users,get_db
from sqlalchemy.inspection import inspect
from passlib.context import CryptContext
from schemas import *
import datetime
import jwt

user_router=APIRouter()
crypt_context=CryptContext(schemes=['bcrypt'],deprecated='auto')
SECRET_KEY = "a_secret_key_for_jwt_token"
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="access_token")

def to_dict(obj):
    return {c.key:getattr(obj,c.key)  for c in inspect(obj).mapper.column_attrs}

def create_access_token(data):
    encode=data.copy()
    exp=datetime.datetime.now()+datetime.timedelta(minutes=60)
    encode['exp']=int(exp.timestamp())
    sec=['created_at','tzinfo']
    to_encode = {key: value for key, value in encode.items() if key not in sec}
    print(to_encode)
    token=jwt.encode(to_encode,SECRET_KEY,ALGORITHM)
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
def auth_user(user:UserAuth,response:Response,db=Depends(get_db))->dict:
    try:
        db_user=db.query(Users).where(Users.email==user.email).one()
        if not user:
            raise HTTPException(status_code=404,detail="Email not registered")
        verified=crypt_context.verify(user.password,db_user.password)
        if not verified:
            raise HTTPException(status_code=401,detail="Password not matched")
        
        token=create_access_token(to_dict(db_user))
        
        response.set_cookie(key='access_token',value=token,expires=datetime.timedelta(minutes=60),httponly=True,secure=True)
        if db_user.is_superadmin:
            response.set_cookie(key="is_superadmin",value="true",expires=datetime.timedelta(minutes=60),httponly=True,secure=True)
        else:
            response.delete_cookie(key="is_superadmin")
        db.close()
        return {'user':to_dict(db_user)}
            
    except Exception as e:
            print(e)
            raise HTTPException(status_code=500,detail="Something went wrong")
        
        
def get_token(request: Request, token: str = Depends(oauth2_scheme)):
    cookie_token = request.cookies.get("access_token")
    return cookie_token or token
        
@user_router.get('/users/me')
def get_current_user(token:str=Depends(get_token)):
    try:
        user=jwt.decode(token,SECRET_KEY,[ALGORITHM])
        print(user)
        if not user['email']:
            raise HTTPException(status_code=404,detail="User not logged in properly")
        return user
                
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500,detail="JWT Exception")
    
@user_router.post('/register')
def register_user(new_user:UserRegister,db=Depends(get_db))->dict:
    try:
        
        user_present=db.query(Users).where(Users.email==new_user.email).one_or_none()
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
    except Exception as e:
        print(e)
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
    
    
def require_role(role:int):
    def role_checker(user=Depends(get_current_user)):
        if user['role_id']==role or user['is_superadmin']:
            return user
        else:
            raise HTTPException(
                status_code=403,
                detail="You don't have permission to access this resource"
            )
        
    return role_checker

@user_router.get('/users/all')
def get_all_users(db=Depends(get_db),user=Depends(require_role(2))):
    try:
        users=db.query(Users).all()
        users_lst=[to_dict(user) for user in users]
        return {'users':users_lst}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500,detail="Something went wrong")
        
        
        
        
        
        
        
    

            
            
            
        
        
             
        
    