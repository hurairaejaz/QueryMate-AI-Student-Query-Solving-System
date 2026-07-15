from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from src.services.dependencies import get_current_user_either
from src.config.database import get_db
from src.services.kb_services import  (
    list_kb_entries,
    search_kb_entries,
    get_kb_entry,
    create_kb_entry,
    update_kb_entry,
    delete_kb_entry,
)

router = APIRouter(prefix="/kb", tags=["Knowledge Base"])


@router.get("/")
def get_all_kb(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    """Get all knowledge base entries"""
    results = list_kb_entries(db, skip=skip, limit=limit)
    return {"items": results, "total": len(results)}


@router.post("/search")
def search_kb(
    query: str = Form(...), 
    department_key: str = Form("software_engineering"), 
    db: Session = Depends(get_db)
):
    """Search knowledge base"""
    results = search_kb_entries(db, query=query, department_key=department_key)
    if results:
        return {"warning": "Content already exists", "matches": results}
    return {"matches": []}


@router.post("/add")
def add_content(
    db: Session = Depends(get_db),

    # Text fields via Form(...)
    department_key: str = Form("software_engineering"),
    title: str = Form(...),
    question: str = Form(...),  # Question from frontend
    answer: str = Form(...),    # Answer from frontend
    category_id: int | None = Form(None),
    tags: str | None = Form(None),
    language: str | None = Form("en"),
    current_user=Depends(get_current_user_either),
    # Optional file
    file: UploadFile | None = File(None),
):
    try:
        # Combine question and answer into content
        content = f"Q: {question}\n\nA: {answer}"
        
        tags_list = [t.strip() for t in tags.split(",")] if tags else None

        kb = create_kb_entry(
            db,
            department_key=department_key,
            title=title,
            content=content,
            category_id=category_id,
            tags=tags_list,
            language=language,
            upload_file=file,
            created_by=current_user["user_id"]
        )

        return {"message": "Content stored successfully", "kb_id": kb.kb_id, "title": kb.title}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
