from typing import Optional

from fastapi import APIRouter, Depends, File, Form, UploadFile, HTTPException, Request
from sqlalchemy.orm import Session

from src.services.escalation_service import respond_to_escalated_query
from src.config.database import get_db
from src.services.dependencies import get_current_user_either
from src.services.kb_services import (
    list_kb_entries,
    search_kb_entries,
    get_kb_entry,
    create_kb_entry,
    update_kb_entry,
    delete_kb_entry,
)

router = APIRouter(
    prefix="/admin/kb",
    tags=["Knowledge Base"],
    dependencies=[Depends(get_current_user_either)],
)

@router.post("/escalations/{query_id}/respond")
def admin_respond_query(
    query_id: int,
    response_text: str = Form(...),
    file: UploadFile | None = File(None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user_either),
):
    responder_id = current_user.get("user_id") if isinstance(current_user, dict) else None

    return respond_to_escalated_query(
        db=db,
        query_id=query_id,
        responder_id=responder_id,
        response_text=response_text,
        file=file,
    )

@router.get("/")
def admin_list_kb(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    """List all KB entries"""
    return list_kb_entries(db, skip=skip, limit=limit)


@router.post("/search")
def admin_search_kb(
    query: str = Form(...),
    department_key: Optional[str] = Form("software_engineering"),
    db: Session = Depends(get_db),
):
    """Search KB entries"""
    return search_kb_entries(db, query=query, department_key=department_key)


@router.get("/{kb_id}")
def admin_get_kb(kb_id: int, db: Session = Depends(get_db)):
    """Get single KB entry"""
    try:
        return get_kb_entry(db, kb_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/")
def admin_create_kb(
    request: Request,
    department_key: str = Form("software_engineering"),
    question: str = Form(...),
    answer: str = Form(...),
    category_id: Optional[int] = Form(None),
    tags: Optional[str] = Form(None),
    language: Optional[str] = Form("en"),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
):
    """Create new KB entry"""

    tags_list = [t.strip() for t in tags.split(",")] if tags else None

    try:
        return create_kb_entry(
            db=db,
            request=request,
            department_key=department_key,
            title=question.strip(),
            content=answer.strip(),
            category_id=category_id,
            tags=tags_list,
            language=language,
            upload_file=file,
        )
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.put("/{kb_id}")
def admin_update_kb(
    kb_id: int,
    request: Request,
    title: Optional[str] = Form(None),
    content: Optional[str] = Form(None),
    category_id: Optional[int] = Form(None),
    tags: Optional[str] = Form(None),
    language: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
):
    """Update KB entry"""

    tags_list = [t.strip() for t in tags.split(",") if t.strip()] if tags else None

    try:
        return update_kb_entry(
            db=db,
            request=request,
            kb_id=kb_id,
            title=title.strip() if title else None,
            content=content.strip() if content else None,
            category_id=category_id,
            tags=tags_list,
            language=language,
            upload_file=file,
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{kb_id}")
def admin_delete_kb(kb_id: int, db: Session = Depends(get_db)):
    """Delete KB entry"""
    try:
        return delete_kb_entry(db, kb_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))