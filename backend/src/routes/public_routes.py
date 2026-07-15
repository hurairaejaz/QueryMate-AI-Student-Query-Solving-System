import os
from urllib.parse import urlparse

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.models.attachements import Attachment

router = APIRouter(tags=["Public"])


@router.get("/public/query/document/{attachment_id}")
def public_download_document(
    attachment_id: int,
    db: Session = Depends(get_db)
):
    attachment = (
        db.query(Attachment)
        .filter(Attachment.attachment_id == attachment_id)
        .first()
    )

    if not attachment:
        raise HTTPException(status_code=404, detail="Document not found")

    file_url = (attachment.file_url or "").strip()

    if not file_url:
        raise HTTPException(status_code=404, detail="Document path not found")

    # CHANGE: Convert DB URL/path into local server file path.
    parsed = urlparse(file_url)

    if parsed.scheme in ["http", "https"]:
        file_path = parsed.path.lstrip("/")
    else:
        file_path = file_url.lstrip("/")

    #  Normalize Window
    file_path = os.path.normpath(file_path)

    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=404,
            detail=f"File not found on server: {file_path}"
        )

    return FileResponse(
        path=file_path,
        filename=attachment.file_name or "document",
        media_type=attachment.mime_type or "application/octet-stream",
    )