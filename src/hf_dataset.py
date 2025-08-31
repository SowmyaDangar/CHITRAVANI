# src/hf_dataset.py
# small functions to upload files to a Hugging Face dataset repo
from huggingface_hub import HfApi, HfFolder, upload_file
import io, json, datetime, uuid

def _save_token(token):
    if token:
        HfFolder.save_token(token)

def push_file(dataset_repo: str, token: str, file_bytes: bytes, file_path: str, metadata: dict):
    """
    dataset_repo: "username/repo-name"
    file_path: path inside the dataset repo like "images/<id>.png" or "videos/<id>.mp4"
    metadata: a dict (will be saved as metadata/<id>.json)
    """
    _save_token(token)
    uid = metadata.get("id", str(uuid.uuid4()))
    # upload the file
    upload_file(path_or_fileobj=io.BytesIO(file_bytes),
                path_in_repo=file_path,
                repo_id=dataset_repo,
                repo_type="dataset",
                token=token)
    # upload metadata JSON
    meta_path = f"metadata/{uid}.json"
    upload_file(path_or_fileobj=io.BytesIO(json.dumps(metadata, ensure_ascii=False).encode('utf-8')),
                path_in_repo=meta_path,
                repo_id=dataset_repo,
                repo_type="dataset",
                token=token)
    return uid
