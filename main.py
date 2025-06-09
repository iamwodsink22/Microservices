from fastapi import FastAPI, Depends, Request
from uuid import uuid4
from fastapi.responses import RedirectResponse,Response, JSONResponse
from gateway.api_gateway import call_api_gateway, RedirectAssetServiceException,RedirectUserServiceException
from users.main import user_app
from assets.main import asset_app
from assetmngmnt import main
from loguru import logger


app=FastAPI()
app.include_router(main.router,dependencies=[Depends(call_api_gateway)],prefix='/app')
app.mount('/users',user_app)
app.mount('/assets',asset_app)

logger.add("info.log",format="Log: [{extra[log_id]}: {time} - {level} - {message} ", level="INFO", enqueue = True)

@app.middleware("http")
async def log_middleware(request:Request, call_next):
    
    log_id = str(uuid4())
    with logger.contextualize(log_id=log_id):
        logger.info('Request to access ' + request.url.path)
        try:
            response = await call_next(request)
        except Exception as ex: 
            logger.error(f"Request to " + request.url.path + " failed: {ex}")
            response = JSONResponse(content={"success": False}, status_code=500)
        finally: 
            logger.info('Successfully accessed ' + request.url.path)
            return response


@app.exception_handler(RedirectUserServiceException)
def redirect_user():
    return RedirectResponse(url='http://localhost:8000/app/users/index')

@app.exception_handler(RedirectAssetServiceException)
def redirect_user():
    return RedirectResponse(url='http://localhost:8000/app/assets/index')