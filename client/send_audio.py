import requests

API_URL = "http://localhost:8000/transcribe"
AUDIO_PATH = "../audio_samples/sample.wav"

with open(AUDIO_PATH, "rb") as f:
    response = requests.post(API_URL, files={"file": f})
    print(response.json())
