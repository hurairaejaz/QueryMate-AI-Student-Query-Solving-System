import os
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException
from src.services.drive_services import upload_file_to_drive

router = APIRouter(prefix="/test-drive", tags=["Test Drive"])


@router.post("/upload")
async def test_drive_upload(file: UploadFile = File(...)):
    allowed_types = [
        "application/pdf",
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ]

    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Only PDF, DOC, and DOCX files are allowed"
        )

    temp_dir = "temp_uploads"
    os.makedirs(temp_dir, exist_ok=True)

    temp_path = os.path.join(temp_dir, file.filename)

    try:
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        await file.close()

        result = upload_file_to_drive(temp_path, file.filename)

        return {
            "message": "Upload successful",
            "file_name": file.filename,
            "content_type": file.content_type,
            "drive_file_id": result["file_id"],
            "file_url": result["file_url"],
            "download_url": result["download_url"]
        }

    except Exception as e:
        print("Drive upload error:", repr(e))
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        try:
            if os.path.exists(temp_path):
                os.remove(temp_path)
        except Exception as cleanup_error:
            print("Temp file cleanup error:", repr(cleanup_error))