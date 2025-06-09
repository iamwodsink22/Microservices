from fastapi import FastAPI,Depends
from configurations.config import AssetSettings,UserSettings,ServerSettings
user_app=FastAPI(debug=True)
from database import engine
from auth import user_router

user_app.include_router(user_router,prefix='/auth')

def build_config(): 
    return UserSettings()

def fetch_config():
    return ServerSettings()

@user_app.get('/index')
def index_faculty(config:UserSettings = Depends(build_config), fconfig:ServerSettings = Depends(fetch_config)): 
    return {
            'project_name': config.application,
            'webmaster': config.webmaster,
            'created': config.created,
            'production_server' : fconfig.production_server,
            'prod_port' : fconfig.prod_port
            }
