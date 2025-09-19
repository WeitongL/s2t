from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from app.stt_engine import transcribe_audio

router = APIRouter()

@router.get("/health")
def health():
    return {"status": "ok"}

@router.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    if file.content_type not in ["audio/wav", "audio/x-wav", "audio/mpeg"]:
        raise HTTPException(status_code=400, detail="Unsupported file format. Only WAV or MP3 allowed.")
    transcript = await transcribe_audio(file)
    if transcript is None:
        return JSONResponse(status_code=500, content={"error": "Transcription failed"})
    return {"transcript": transcript}
