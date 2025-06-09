import logging
from fastapi import Request

logger = logging.getLogger('uvicorn.access')

def call_api_gateway(request:Request):
    id=request.path_params['portal_id']
    if id==str(1):
        raise RedirectUserServiceException
    elif id==str(2):
        raise RedirectAssetServiceException
    
class RedirectUserServiceException(Exception):
    pass

class RedirectAssetServiceException(Exception):
    pass
        