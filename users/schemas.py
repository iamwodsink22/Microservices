from pydantic import BaseModel

class UserAuth(BaseModel):
    email:str
    password:str
    
class UserRegister(BaseModel):
    email:str
    name:str
    password:str