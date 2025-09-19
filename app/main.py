from fastapi import FastAPI
from app.api import router
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

# Serve static files (JS, CSS, etc) from /static under /static/
app.mount("/static", StaticFiles(directory="static"), name="static")


# Redirect "/" to your index.html (not /docs)
@app.get("/", include_in_schema=False)
async def root():
    return FileResponse(os.path.join("static", "index.html"))
app = FastAPI(title="Speech-to-Text Service")
app.include_router(router)
