# src/utils.py
# tiny helpers: convert bytes to base64 and back, create payload dictionary
import base64, uuid, datetime

def bytes_to_b64(b: bytes) -> str:
    return base64.b64encode(b).decode('utf-8')

def b64_to_bytes(s: str) -> bytes:
    return base64.b64decode(s)

def make_payload(file_bytes: bytes, file_type: str, caption: str, language: str, region: str, category: str, consent: str):
    """Make a notebook-friendly record to save later"""
    return {
        "id": str(uuid.uuid4()),
        "type": file_type,           # "image" or "video"
        "caption": caption,
        "language": language,
        "region": region,
        "category": category,
        "consent": consent,
        "created_at": datetime.datetime.utcnow().isoformat() + "Z",
        "data_b64": bytes_to_b64(file_bytes)
    }
