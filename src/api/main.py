from fastapi import FastAPI
from src.api.endpoints import router

app = FastAPI()
app.include_router(router)