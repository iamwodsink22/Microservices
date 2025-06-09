from fastapi import FastAPI, Depends
from assets.actions import crud_router
from configurations.config import ServerSettings,AssetSettings
asset_app=FastAPI()
asset_app.include_router('/actions',crud_router)
def build_config(): 
    return AssetSettings()

def fetch_config():
    return ServerSettings()

@asset_app.get('/index')
def index_faculty(config:AssetSettings = Depends(build_config), fconfig:ServerSettings = Depends(fetch_config)): 
    return {
            'project_name': config.application,
            'webmaster': config.webmaster,
            'created': config.created,
            'production_server' : fconfig.production_server,
            'prod_port' : fconfig.prod_port
            }
