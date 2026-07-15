from typing import Optional
from fastapi import UploadFile
from sqlalchemy.orm import Session

from src.models.kb_content import KBContent
from src.schemas.kb_content import KBContentCreate, KBContentUpdate
from src.services.drive_services import upload_file_to_drive


def _tags_to_string(tags: list[str] | None) -> str | None:
    if not tags:
        return None
    cleaned = [t.strip() for t in tags if t and t.strip()]
    return ",".join(cleaned) if cleaned else None


def create_kb_entry(db: Session, data: KBContentCreate, file: Optional[UploadFile] = None) -> KBContent:
    file_url = None
    file_name = None
    file_mime = None

    #  Admin pipeline: NO AI validation
    if file is not None:
        file_bytes = file.file.read()
        file_name = file.filename
        file_mime = file.content_type or "application/octet-stream"

        file_url = upload_file_to_drive(
            filename=file_name,
            content_type=file_mime,
            file_bytes=file_bytes,
        )

    kb = KBContent(
        department_id=data.department_id,
        title=data.title.strip(),
        question=data.question.strip(),
        answer=data.answer.strip(),
        tags=_tags_to_string(data.tags),
        language=(data.language or "en"),
        file_url=file_url,
        file_name=file_name,
        file_mime=file_mime,
        is_active=True,
    )

    db.add(kb)
    db.commit()
    db.refresh(kb)
    return kb


def update_kb_entry(
    db: Session,
    kb_id: int,
    data: KBContentUpdate,
    file: Optional[UploadFile] = None
) -> KBContent:
    kb = db.query(KBContent).filter(KBContent.id == kb_id, KBContent.is_active == True).first()
    if not kb:
        raise ValueError("KB entry not found")

    # Text updates (only if provided)
    if data.department_id is not None:
        kb.department_id = data.department_id
    if data.title is not None:
        kb.title = data.title.strip()
    if data.question is not None:
        kb.question = data.question.strip()
    if data.answer is not None:
        kb.answer = data.answer.strip()
    if data.tags is not None:
        kb.tags = _tags_to_string(data.tags)
    if data.language is not None:
        kb.language = data.language

    # File removal
    if getattr(data, "remove_file", False):
        kb.file_url = None
        kb.file_name = None
        kb.file_mime = None

    #  File replacement upload
    if file is not None:
        file_bytes = file.file.read()
        file_name = file.filename
        file_mime = file.content_type or "application/octet-stream"

        file_url = upload_file_to_drive(
            filename=file_name,
            content_type=file_mime,
            file_bytes=file_bytes,
        )

        kb.file_url = file_url
        kb.file_name = file_name
        kb.file_mime = file_mime

    db.commit()
    db.refresh(kb)
    return kb