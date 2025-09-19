import os

import requests

API_URL = "http://localhost:8000/transcribe"
AUDIO_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "audio_samples", "sample.wav")
with open(AUDIO_PATH, "rb") as f:
    response = requests.post(API_URL, files={"file": f})
    print(response.json())
