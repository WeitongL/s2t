import tempfile
from faster_whisper import WhisperModel

model = WhisperModel("base", device="cpu", compute_type="int8")

async def transcribe_audio(upload_file):
    with tempfile.NamedTemporaryFile(delete=True, suffix=".wav") as tmp:
        tmp.write(await upload_file.read())
        tmp.flush()
        segments, info = model.transcribe(tmp.name)
        text = " ".join([segment.text for segment in segments])
        return text
