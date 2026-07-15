from fastapi import UploadFile, Request
from sqlalchemy.orm import Session
from sqlalchemy import text
from urllib.parse import urlparse
import os
import shutil
import uuid
from sqlalchemy import text
from src.models.attachements import Attachment
from src.models.kb_content import KnowledgeBase

UPLOAD_DIR = "uploads/documents"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def save_uploaded_file(file: UploadFile, base_url: str):
    """
    Save uploaded file locally and return file metadata.
    """
    if not file or not file.filename:
        return None

    original_name = file.filename.strip()
    ext = os.path.splitext(original_name)[1]
    unique_name = f"{uuid.uuid4().hex}{ext}"
    file_path = os.path.join(UPLOAD_DIR, unique_name)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    file_url = f"{base_url}/{file_path.replace(os.sep, '/')}"

    return {
        "file_name": original_name,
        "stored_name": unique_name,
        "file_path": file_path,
        "file_url": file_url,
        "mime_type": file.content_type,
    }


def get_local_path_from_url(file_url: str):
    """
    Convert stored file_url back to local file path for deletion.
    Example:
    http://127.0.0.1:8000/uploads/documents/abc.pdf
    -> uploads/documents/abc.pdf
    """
    if not file_url:
        return None

    try:
        parsed = urlparse(file_url)
        relative_path = parsed.path.lstrip("/")  # uploads/documents/abc.pdf
        return os.path.normpath(relative_path)
    except Exception as e:
        print(f"Error parsing file_url to local path: {e}")
        return None


def delete_local_file(file_path: str):
    """
    Delete physical file from local storage using file path.
    """
    if not file_path:
        return

    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        print(f"Error deleting file from disk: {e}")


def list_kb_entries(db: Session, skip: int = 0, limit: int = 50):
    rows = db.query(KnowledgeBase).offset(skip).limit(limit).all()

    return [
        {
            "kb_id": kb.kb_id,
            "title": kb.title,
            "content": kb.content,
            "department_key": kb.department_key,
            "attachments": [
                {
                    "id": att.attachment_id,
                    "file_name": att.file_name,
                    "file_url": att.file_url,
                    "mime_type": att.mime_type,
                }
                for att in kb.attachments
            ],
        }
        for kb in rows
    ]


def search_kb_entries(db: Session, query: str, department_key: str = "software_engineering"):
    rows = (
        db.query(KnowledgeBase)
        .filter(
            KnowledgeBase.department_key == department_key,
            (
                KnowledgeBase.title.ilike(f"%{query}%")
                | KnowledgeBase.content.ilike(f"%{query}%")
            ),
        )
        .order_by(KnowledgeBase.kb_id.asc())
        .all()
    )

    return [
        {
            "kb_id": kb.kb_id,
            "title": kb.title,
            "content": kb.content,
            "department_key": kb.department_key,
            "attachments": [
                {
                    "id": att.attachment_id,
                    "file_name": att.file_name,
                    "file_url": att.file_url,
                    "mime_type": att.mime_type,
                }
                for att in kb.attachments
            ],
        }
        for kb in rows
    ]


def get_kb_entry(db: Session, kb_id: int):
    kb = db.query(KnowledgeBase).filter(KnowledgeBase.kb_id == kb_id).first()
    if not kb:
        raise ValueError("KB entry not found")

    return {
        "kb_id": kb.kb_id,
        "title": kb.title,
        "content": kb.content,
        "department_key": kb.department_key,
        "attachments": [
            {
                "id": att.attachment_id,
                "file_name": att.file_name,
                "file_url": att.file_url,
                "mime_type": att.mime_type,
            }
            for att in kb.attachments
        ],
    }


def create_kb_entry(
    db: Session,
    request: Request,
    department_key: str,
    title: str,
    content: str,
    category_id: int = None,
    tags: list = None,
    language: str = "en",
    upload_file: UploadFile = None,
):
    existing = (
        db.query(KnowledgeBase)
        .filter(
            KnowledgeBase.title == title,
            KnowledgeBase.department_key == department_key,
        )
        .first()
    )

    if existing:
        raise ValueError("KB entry with this question already exists.")

    kb = KnowledgeBase(
        department_key=department_key,
        title=title,
        content=content,
        category_id=category_id,
    )

    db.add(kb)
    db.commit()
    db.refresh(kb)

    if upload_file:
        base_url = str(request.base_url).rstrip("/")
        file_data = save_uploaded_file(upload_file, base_url)

        attachment = Attachment(
            kb_id=kb.kb_id,
            file_name=file_data["file_name"],
            file_url=file_data["file_url"],
            mime_type=file_data["mime_type"],
            drive_file_id=None,
        )
        db.add(attachment)
        db.commit()
        db.refresh(kb)

    refresh_kb_search_vector(db, kb.kb_id)

    return {
        "message": "KB entry created successfully",
        "kb_id": kb.kb_id,
        "title": kb.title,
        "content": kb.content,
        "department_key": kb.department_key,
        "attachments": [
            {
                "id": att.attachment_id,
                "file_name": att.file_name,
                "file_url": att.file_url,
                "mime_type": att.mime_type,
            }
            for att in kb.attachments
        ],
    }


def update_kb_entry(
    db: Session,
    request: Request,
    kb_id: int,
    title: str = None,
    content: str = None,
    category_id: int = None,
    tags: list = None,
    language: str = None,
    upload_file: UploadFile = None,
):
    kb = db.query(KnowledgeBase).filter(KnowledgeBase.kb_id == kb_id).first()
    if not kb:
        raise ValueError("KB entry not found")

    if title is not None:
        kb.title = title
    if content is not None:
        kb.content = content
    if category_id is not None:
        kb.category_id = category_id

    if upload_file:
        old_attachment = (
            db.query(Attachment)
            .filter(Attachment.kb_id == kb.kb_id)
            .first()
        )

        if old_attachment:
            old_file_path = get_local_path_from_url(old_attachment.file_url)
            delete_local_file(old_file_path)
            db.delete(old_attachment)
            db.commit()

        base_url = str(request.base_url).rstrip("/")
        file_data = save_uploaded_file(upload_file, base_url)

        new_attachment = Attachment(
            kb_id=kb.kb_id,
            file_name=file_data["file_name"],
            file_url=file_data["file_url"],
            mime_type=file_data["mime_type"],
            drive_file_id=None,
        )
        db.add(new_attachment)

    db.commit()
    db.refresh(kb)

    refresh_kb_search_vector(db, kb.kb_id)

    return {
        "message": "KB entry updated successfully",
        "kb_id": kb.kb_id,
        "title": kb.title,
        "content": kb.content,
        "department_key": kb.department_key,
        "attachments": [
            {
                "id": att.attachment_id,
                "file_name": att.file_name,
                "file_url": att.file_url,
                "mime_type": att.mime_type,
            }
            for att in kb.attachments
        ],
    }


def refresh_kb_search_vector(db: Session, kb_id: int):
    sql = text("""
        UPDATE software_engineering.knowledge_base
        SET search_vector = to_tsvector(
            'english',
            coalesce(title, '') || ' ' || coalesce(content, '')
        )
        WHERE kb_id = :kb_id
    """)
    db.execute(sql, {"kb_id": kb_id})
    db.commit()


def delete_kb_entry(db: Session, kb_id: int):
    kb = db.query(KnowledgeBase).filter(KnowledgeBase.kb_id == kb_id).first()

    if not kb:
        raise ValueError("KB entry not found")

    try:
        # 1. Delete KB chunks if table/model exists
        try:
            from src.models.kb_chunks import KBChunk
            db.query(KBChunk).filter(KBChunk.kb_id == kb_id).delete(
                synchronize_session=False
            )
            db.flush()
        except Exception as e:
            db.rollback()
            print(f"KB chunks delete skipped: {e}")

        # Reload KB after rollback
        kb = db.query(KnowledgeBase).filter(KnowledgeBase.kb_id == kb_id).first()
        if not kb:
            return {
                "message": "KB entry already deleted",
                "kb_id": kb_id
            }

        # 2. Delete embeddings only if table exists
        embeddings_table = db.execute(
            text("SELECT to_regclass('software_engineering.kb_embeddings')")
        ).scalar()

        if embeddings_table:
            db.execute(
                text("DELETE FROM software_engineering.kb_embeddings WHERE kb_id = :kb_id"),
                {"kb_id": kb_id}
            )
            db.flush()

        # 3. Delete attachments + physical files
        old_attachments = db.query(Attachment).filter(
            Attachment.kb_id == kb_id
        ).all()

        for att in old_attachments:
            old_file_path = get_local_path_from_url(att.file_url)
            delete_local_file(old_file_path)
            db.delete(att)

        db.flush()

        # 4. Delete main KB row
        db.delete(kb)
        db.commit()

        return {
            "message": "KB entry and related documents deleted successfully",
            "kb_id": kb_id
        }

    except Exception as e:
        db.rollback()
        print(f"Delete KB failed: {e}")
        raise e