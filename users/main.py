from fastapi import FastAPI
app=FastAPI(debug=True)
from database import engine
from auth import user_router

app.include_router(user_router,prefix='/auth')
