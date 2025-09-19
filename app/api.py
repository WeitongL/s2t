import os

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from app.stt_engine import transcribe_audio

router = APIRouter()
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

# Serve static files (JS, CSS, etc) from /static under /static/
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
# Redirect "/" to your index.html (not /docs)
@app.get("/")
def read_index():
    return FileResponse("static/index.html")
@router.get("/health")
def health():
    return {"status": "ok"}
SUPPORTED_TYPES = ["audio/wav", "audio/x-wav", "audio/mpeg"]
SUPPORTED_EXTENSIONS = [".wav", ".mp3"]

@router.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename)[-1].lower()
    if (file.content_type not in SUPPORTED_TYPES) and (ext not in SUPPORTED_EXTENSIONS):
        raise HTTPException(
            status_code=400,
            detail="Unsupported file format. Only WAV or MP3 allowed."
        )
    transcript = await transcribe_audio(file)
    if transcript is None:
        return JSONResponse(status_code=500, content={"error": "Transcription failed"})
    return {"transcript": transcript}