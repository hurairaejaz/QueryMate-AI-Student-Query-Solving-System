import os
import time
import shutil
from fastapi import UploadFile, HTTPException

UPLOAD_DIR = "uploads/kb_files"
ALLOWED_EXTENSIONS = {".pdf", ".doc", ".docx"}


def ensure_upload_dir():
    os.makedirs(UPLOAD_DIR, exist_ok=True)


def validate_file(upload_file: UploadFile):
    ext = os.path.splitext(upload_file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only PDF, DOC, and DOCX files are allowed."
        )


def save_file_locally(upload_file: UploadFile, base_url: str):
    ensure_upload_dir()
    validate_file(upload_file)

    safe_name = upload_file.filename.replace(" ", "_")
    stored_name = f"{int(time.time())}_{safe_name}"
    full_path = os.path.join(UPLOAD_DIR, stored_name)

    with open(full_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)

    relative_path = f"{UPLOAD_DIR}/{stored_name}".replace("\\", "/")
    file_url = f"{base_url}/{relative_path}"

    return {
        "file_name": upload_file.filename,
        "stored_name": stored_name,
        "file_path": relative_path,
        "file_url": file_url,
        "mime_type": upload_file.content_type,
    }


def delete_local_file(file_path: str):
    if file_path and os.path.exists(file_path):
        os.remove(file_path)