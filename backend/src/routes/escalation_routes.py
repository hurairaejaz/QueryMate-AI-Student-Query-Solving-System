from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi import UploadFile
# from src.models.query_event import QueryEvent
from src.models.response import Response
from src.models.attachements import Attachment
from src.services.kb_services import save_uploaded_file
from src.config.database import get_db
from src.services.dependencies import get_current_user_either
from src.models.query import Query
from src.models.notification import Notification
from src.models.user import Users
from src.services.email_service import send_email
from src.services.whatsapp_service import send_whatsapp_text
from src.services.escalation_service import (
    assign_query_to_staff,
    respond_to_escalated_query as submit_escalated_response,
    mark_query_resolved,
)
from src.models.query import Query
from src.models.whatsapp_user import WhatsAppUsers
from src.models.attachements import Attachment
from src.services.whatsapp_service import (
    send_whatsapp_text,
    send_whatsapp_document,
    upload_whatsapp_media,
    convert_file_url_to_path,
)
import os
from src.services.notification_service import (
    notify_query_assigned,
    notify_query_resolved,
)
from src.schemas.escalation import (
    AssignQueryRequest,
    EscalatedResponseCreate,
    ResolveQueryRequest,
)

router = APIRouter(prefix="/admin/escalations", tags=["Escalations"])


# @router.get("/")
@router.get("/")
def list_escalated_queries(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user_either),
):
    queries = (
        db.query(Query)
        .filter(Query.status.in_(["escalated", "assigned"]))
        .order_by(Query.created_at.desc())
        .all()
    )

    items = []

    for q in queries:
        student = None
        assigned_staff = None
        # CHANGE: WhatsApp queries usually do not have student email, so get WhatsApp phone
        whatsapp_phone = None
        if q.source == "whatsapp" and q.whatsapp_user:
            whatsapp_phone = q.whatsapp_user.phone_number
            
        if q.student_user_id:
            student = db.query(Users).filter(Users.user_id == q.student_user_id).first()

        if q.assigned_to:
            assigned_staff = db.query(Users).filter(Users.user_id == q.assigned_to).first()

        latest_response = ""
        if q.responses:
            latest_response = q.responses[-1].response_text or ""

        items.append({
            "query_id": q.query_id,
            "student_name": student.full_name if student else "N/A",
            "student_email": student.email if student else "N/A",
            "whatsapp_phone": q.whatsapp_user.phone_number
            if q.source == "whatsapp" and q.whatsapp_user
            else None,
            "query_text": q.query_text,
            "category": q.intent_label or "General",
            "source": q.source.title() if q.source else "Unknown",
            "status": q.status.capitalize() if q.status else "Unknown",
            "confidence_score": q.confidence_score,
            "escalation_reason": q.escalation_reason,
            "assigned_to": q.assigned_to,
            "assigned_to_name": assigned_staff.full_name if assigned_staff else "",
            "assigned_to_email": assigned_staff.email if assigned_staff else "",
            "created_at": q.created_at.strftime("%Y-%m-%d %I:%M %p") if q.created_at else "",
            "response_text": latest_response,
            "student_user_id": q.student_user_id,
        })

    return items


@router.get("/{query_id}")
def get_escalated_query_detail(
    query_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user_either),
):
    q = db.query(Query).filter(Query.query_id == query_id).first()

    if not q:
        raise HTTPException(status_code=404, detail="Query not found")

    documents = []
    if q.matched_attachment:
        att = q.matched_attachment
        documents.append({
            "attachment_id": att.attachment_id,
            "file_name": att.file_name,
            "file_type": att.file_type,
            "mime_type": att.mime_type,
            "open_url": f"/app/query/document/{att.attachment_id}",
            "download_url": f"/app/query/document/{att.attachment_id}",
            "file_url": att.file_url,
        })
    whatsapp_phone = None
    if q.source == "whatsapp" and q.whatsapp_user:
        whatsapp_phone = q.whatsapp_user.phone_number
        
    return {
        "query_id": q.query_id,
        "query_text": q.query_text,
        "normalized_text": q.normalized_text,
        "detected_language": q.detected_language,
        "intent_label": q.intent_label,
        "source": q.source,
        "status": q.status,
        "ai_response": q.ai_response,
        "confidence_score": q.confidence_score,
        "escalation_reason": q.escalation_reason,
        "assigned_to": q.assigned_to,
        "resolution_type": q.resolution_type,
        "created_at": q.created_at,
        "whatsapp_phone": whatsapp_phone,
        "documents": documents,
        "events": [
            {
                "event_id": e.event_id,
                "event_type": e.event_type,
                "event_message": e.event_message,
                "created_by": e.created_by,
                "created_at": e.created_at,
            }
            for e in q.events
        ],
        "responses": [
            {
                "response_id": r.response_id,
                "response_text": r.response_text,
                "response_type": r.response_type,
                "responder_id": r.responder_id,
                "attachment_id": r.attachment_id,
                "created_at": r.created_at,
            }
            for r in q.responses
        ],
    }


@router.post("/{query_id}/assign")
def assign_escalated_query(
    query_id: int,
    payload: AssignQueryRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user_either),
):
    try:
        assignment = assign_query_to_staff(
            db=db,
            query_id=query_id,
            assigned_to=payload.assigned_to,
            assigned_by=current_user.get("user_id"),
            notes=payload.notes,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if not assignment:
        raise HTTPException(status_code=404, detail="Query not found")

    query_obj = db.query(Query).filter(Query.query_id == query_id).first()
    if query_obj:
        notify_query_assigned(
        db=db,
        query_obj=query_obj,
        assigned_staff_email=payload.assigned_to_email,
        assigned_staff_name=payload.assigned_to_name,
    )
    if query_obj.source == "whatsapp" and query_obj.whatsapp_user:
            staff_name = payload.assigned_to_name or "a staff member"

            send_whatsapp_text(
                query_obj.whatsapp_user.phone_number,
                f"Your query has been assigned to {staff_name}. You will receive a response soon."
            )
    return {
        "message": "Query assigned successfully.",
        "assignment_id": assignment.assignment_id,
        "query_id": assignment.query_id,
        "assigned_to": assignment.assigned_to,
        "status": assignment.status,
    }


@router.post("/{query_id}/respond", response_model=None)
def respond_escalated_query(
    query_id: int,
    response_text: str = Form(...),
    file: UploadFile | None = File(None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user_either),
):
    try:
        responder_id = current_user.get("user_id") if isinstance(current_user, dict) else None

        response = submit_escalated_response(
            db=db,
            query_id=query_id,
            responder_id=responder_id,
            response_text=response_text,
            file=file,
        )

        if not response:
            raise HTTPException(status_code=404, detail="Query not found")

        query_obj = db.query(Query).filter(Query.query_id == query_id).first()

        if not query_obj:
            raise HTTPException(status_code=404, detail="Query not found after response")

        # Get attachment from admin response first, then fallback to query matched attachment.
        attachment = None

        if getattr(response, "attachment_id", None):
            attachment = (
                db.query(Attachment)
                .filter(Attachment.attachment_id == response.attachment_id)
                .first()
            )

        if not attachment and getattr(query_obj, "matched_attachment_id", None):
            attachment = (
                db.query(Attachment)
                .filter(Attachment.attachment_id == query_obj.matched_attachment_id)
                .first()
            )

        if query_obj.source == "whatsapp" and query_obj.whatsapp_user:
            #  Send admin response text to WhatsApp user.
            send_whatsapp_text(
                query_obj.whatsapp_user.phone_number,
                response_text,
            )

            #  If response has document, upload it to Meta and send as real WhatsApp attachment.
            if attachment:
                try:
                    file_path = convert_file_url_to_path(attachment.file_url)

                    if not os.path.exists(file_path):
                        raise Exception(f"File not found on server: {file_path}")

                    media_id = upload_whatsapp_media(
                        file_path=file_path,
                        mime_type=attachment.mime_type or "application/octet-stream",
                    )

                    send_whatsapp_document(
                        to_number=query_obj.whatsapp_user.phone_number,
                        media_id=media_id,
                        file_name=attachment.file_name or "document",
                        caption="Please find the attached document.",
                    )

                except Exception as e:
                    print("WhatsApp admin document send error:", e)

                    #  Fallback link if direct WhatsApp attachment fails.
                    fallback_link = f"/public/query/document/{attachment.attachment_id}"

                    send_whatsapp_text(
                        query_obj.whatsapp_user.phone_number,
                        f"Document could not be attached directly. Please open it here:\n{fallback_link}",
                    )

        elif query_obj.student_user_id:
            notify_query_resolved(
                db=db,
                query_obj=query_obj,
                response_text=response_text,
            )
        else:
            raise HTTPException(
                status_code=400,
                detail="No student account or WhatsApp user found for this query."
            )

        #  Keep app/email notification after WhatsApp handling.
        notify_query_resolved(
            db=db,
            query_obj=query_obj,
            response_text=response_text,
        )

        return {
            "message": "Response submitted successfully.",
            "query_id": query_id,
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{query_id}/resolve")
def resolve_escalated_query(
    query_id: int,
    payload: ResolveQueryRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user_either),
):
    query_obj = mark_query_resolved(
        db=db,
        query_id=query_id,
        responder_id=current_user.get("user_id"),
        notes=payload.notes,
    )

    if not query_obj:
        raise HTTPException(status_code=404, detail="Query not found")
    if query_obj.source == "whatsapp" and query_obj.whatsapp_user:
        send_whatsapp_text(
            query_obj.whatsapp_user.phone_number,
            "Your query has been resolved. Thank you for using QueryMate."
        )

    elif query_obj.student_user_id:
        notify_query_resolved(db, query_obj)
    # if query_obj.student_user_id:
    #     notify_query_resolved(db, query_obj)

    return {
        "message": "Query marked as resolved.",
        "query_id": query_obj.query_id,
        "status": query_obj.status,
    }