import os
import uuid
import json
import requests
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential

load_dotenv()

SPEECH_ENDPOINT = os.getenv("SPEECH_ENDPOINT")
SUBSCRIPTION_KEY = os.getenv("SUBSCRIPTION_KEY")
API_VERSION = "2024-04-15-preview"
PASSWORDLESS_AUTHENTICATION = False

def _authenticate():
    if PASSWORDLESS_AUTHENTICATION:
        credential = DefaultAzureCredential()
        token = credential.get_token("https://cognitiveservices.azure.com/.default")
        return {"Authorization": f"Bearer {token.token}"}
    else:
        return {"Ocp-Apim-Subscription-Key": SUBSCRIPTION_KEY}

def submit_job(text):
    job_id = str(uuid.uuid4())
    url = f"{SPEECH_ENDPOINT}/avatar/batchsyntheses/{job_id}?api-version={API_VERSION}"
    headers = {"Content-Type": "application/json"}
    headers.update(_authenticate())

    payload = {
        "synthesisConfig": {"voice": "en-US-JennyMultilingualNeural"},
        "inputKind": "plainText",
        "inputs": [{"content": text}],
        "avatarConfig": {
            "customized": False,
            "talkingAvatarCharacter": "lisa",
            "talkingAvatarStyle": "casual-sitting",
            "videoFormat": "mp4",
            "videoCodec": "h264",
            "subtitleType": "soft_embedded",
            "backgroundColor": "#FFFFFFFF"
        }
    }

    r = requests.put(url, json.dumps(payload), headers=headers)
    r.raise_for_status()
    return job_id

def check_job_status(job_id):
    url = f"{SPEECH_ENDPOINT}/avatar/batchsyntheses/{job_id}?api-version={API_VERSION}"
    headers = _authenticate()
    r = requests.get(url, headers=headers)
    r.raise_for_status()

    data = r.json()
    status = data.get("status")
    video_url = None
    if status == "Succeeded":
        video_url = data["outputs"]["result"]
    return status, video_url
