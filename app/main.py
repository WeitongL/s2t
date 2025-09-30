from fastapi import FastAPI, Request, HTTPException
import time
from app.api import router

app = FastAPI(title="Speech-to-Text Service")
app.include_router(router)

import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
INDEX_PATH = os.path.join(STATIC_DIR, "index.html")

if os.path.isdir(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
else:
    print(f"Warning: Static directory {STATIC_DIR} not found")


@app.get("/", response_class=FileResponse)
def serve_index():
    if os.path.isfile(INDEX_PATH):
        return FileResponse(INDEX_PATH)
    raise HTTPException(status_code=404, detail="Index file not found")


request_log = {}
RATE_LIMIT = 10  # max requests
WINDOW = 60  # seconds

@app.middleware("http")
async def ddos_protection(request: Request, call_next):
    ip = request.client.host
    now = time.time()

    timestamps = request_log.get(ip, [])
    # Keep only recent requests
    timestamps = [t for t in timestamps if now - t < WINDOW]
    timestamps.append(now)

    request_log[ip] = timestamps

    if len(timestamps) > RATE_LIMIT:
        raise HTTPException(status_code=429, detail="Too many requests")

    response = await call_next(request)
    return response