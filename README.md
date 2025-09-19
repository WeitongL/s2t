# Speech-to-Text Service

## Architecture Overview
Python/FastAPI app for open-source audio transcription using [faster-whisper]. Docker+CI/CD ready.

## Local Setup

```bash
git clone <repo>
cd s2t
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Running with Docker

```bash
docker-compose up --build
```

## Running Tests

```bash
pytest
```

## Example Usage

```bash
curl http://localhost:8000/health
curl -F "file=@audio_samples/sample.wav" http://localhost:8000/transcribe
python client/send_audio.py
```

## Deployment Steps

1. Copy repo to server.
2. Run `docker-compose up --build -d`

## Improvements / Notes

- Add more robust input format detection and conversion.
- Add authentication, storage, better logging.
