from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse
import os

from src.config.database import get_db
from src.services.dependencies import get_current_user_either
from src.services.query_service import submit_app_query, get_student_query_history
from src.models.query import Query
from src.models.attachements import Attachment

router = APIRouter(prefix="/app/query", tags=["App Query"])


@router.post("/submit")
def submit_query(
    payload: dict,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user_either),
):
    user_id = (
    current_user.get("user_id")
    or current_user.get("id")
    or current_user.get("sub")
)

    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid user token: user_id missing")

    query_text = (payload.get("query_text") or "").strip()

    if not query_text:
        raise HTTPException(status_code=400, detail="query_text is required")

    result = submit_app_query(
        db=db,
        student_user_id=user_id,
        query_text=query_text,
    )

    return result


@router.get("/history")
def get_query_history(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user_either),
):
    queries = get_student_query_history(
        db=db,
        student_user_id=current_user.get("user_id"),
    )

    results = []

    for q in queries:
        latest_response = q.responses[-1].response_text if q.responses else None

        results.append({
            "query_id": q.query_id,
            "query_text": q.query_text,
            "status": q.status,
            "source": q.source,
            "created_at": q.created_at,
            "answer": latest_response,
            "confidence_score": q.confidence_score,
            "resolution_type": q.resolution_type,
        })

    return {"items": results, "total": len(results)}


@router.get("/document/{attachment_id}")
def get_query_document(
    attachment_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user_either),
):
    attachment = (
        db.query(Attachment)
        .filter(Attachment.attachment_id == attachment_id)
        .first()
    )

    if not attachment:
        raise HTTPException(status_code=404, detail="Document not found")

    file_path = attachment.file_url

    if not file_path:
        raise HTTPException(status_code=404, detail="File path missing")

    # If saved as full URL, convert to local uploads path
    if file_path.startswith("http"):
        if "uploads/" in file_path:
            file_path = file_path.split("uploads/")[-1]
            file_path = os.path.join("uploads", file_path)
        else:
            raise HTTPException(status_code=404, detail="Invalid file URL")

    # Normalize Windows
    file_path = file_path.replace("\\", os.sep).replace("/", os.sep)

    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=404,
            detail=f"File not found on server: {file_path}"
        )

    file_name = attachment.file_name or os.path.basename(file_path)

    return FileResponse(
        path=file_path,
        filename=file_name,
        media_type=attachment.mime_type or "application/octet-stream",
    )

# PUBLIC ROUTE FOR WHATSAPP (NO AUTH)
@router.get("/public/query/document/{attachment_id}")
def public_download_document(attachment_id: int, db: Session = Depends(get_db)):
    attachment = (
        db.query(Attachment)
        .filter(Attachment.attachment_id == attachment_id)
        .first()
    )

    if not attachment:
        raise HTTPException(status_code=404, detail="Document not found")

    file_path = attachment.file_url

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(
        path=file_path,
        filename=attachment.file_name,
        media_type=attachment.mime_type or "application/octet-stream",
    ) 
    
@router.get("/{query_id}")
def get_query_detail(
    query_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user_either),
):
    query_obj = (
        db.query(Query)
        .filter(
            Query.query_id == query_id,
            Query.student_user_id == current_user.get("user_id"),
        )
        .first()
    )

    if not query_obj:
        raise HTTPException(status_code=404, detail="Query not found")

    documents = []

    if query_obj.matched_attachment:
        att = query_obj.matched_attachment

        documents.append({
            "attachment_id": att.attachment_id,
            "file_name": att.file_name,
            "file_type": att.file_type,
            "mime_type": att.mime_type,
            "open_url": f"/app/query/document/{att.attachment_id}",
            "download_url": f"/app/query/document/{att.attachment_id}",
            "file_url": att.file_url,
        })

    return {
        "query_id": query_obj.query_id,
        "query_text": query_obj.query_text,
        "normalized_text": query_obj.normalized_text,
        "detected_language": query_obj.detected_language,
        "intent_label": query_obj.intent_label,
        "status": query_obj.status,
        "source": query_obj.source,
        "ai_response": query_obj.ai_response,
        "confidence_score": query_obj.confidence_score,
        "escalation_reason": query_obj.escalation_reason,
        "resolution_type": query_obj.resolution_type,
        "created_at": query_obj.created_at,
        "last_response_at": query_obj.last_response_at,
        "documents": documents,
    }
    
