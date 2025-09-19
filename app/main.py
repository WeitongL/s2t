from fastapi import FastAPI
from app.api import router

app = FastAPI(title="Speech-to-Text Service")
app.include_router(router)
