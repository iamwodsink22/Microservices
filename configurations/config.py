from pydantic import BaseSettings
from datetime import date
import os
class UserSettings(BaseSettings): 
    application:str = 'User Service' 
    webmaster:str = 'sjctrags@university.com'
    created:date = '2025-06-09' 
 

class AssetSettings(BaseSettings): 
    application:str = 'Asset Service' 
    webmaster:str = 'sjctrags@university.com'
    created:date = '2025-06-09'
    
class ServerSettings(BaseSettings): 
    production_server:str
    prod_port:int
    development_server:str 
    dev_port:int
    
    class Config: 
        env_file = os.getcwd() + '/configuration/erp_settings.properties'