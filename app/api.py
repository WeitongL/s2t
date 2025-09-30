import os
from fastapi import APIRouter, UploadFile, File, HTTPException, FastAPI
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from app.stt_engine import transcribe_audio

router = APIRouter()

SUPPORTED_TYPES = ["audio/wav", "audio/x-wav", "audio/mpeg"]
SUPPORTED_EXTENSIONS = [".wav", ".mp3"]
# MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

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
    # content = await file.read()
    # if len(content) > MAX_FILE_SIZE:
    #     raise HTTPException(
    #         status_code=413,
    #         detail="File size exceeds 5 MB limit."
    #     )

    transcript = await transcribe_audio(file)
    if transcript is None:
        return JSONResponse(status_code=500, content={"error": "Transcription failed"})
    return {"transcript": transcript}

