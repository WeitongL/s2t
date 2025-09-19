import os
from fastapi import APIRouter, UploadFile, File, HTTPException, FastAPI
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from app.stt_engine import transcribe_audio

router = APIRouter()

SUPPORTED_TYPES = ["audio/wav", "audio/x-wav", "audio/mpeg"]
SUPPORTED_EXTENSIONS = [".wav", ".mp3"]

@router.get("/health")
def health():
    return {"status": "ok"}

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


import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

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