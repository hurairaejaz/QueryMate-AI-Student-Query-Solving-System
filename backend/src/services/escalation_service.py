from fastapi import UploadFile
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from src.models.attachements import Attachment
from src.models.user import Users
from src.services.email_service import send_email
from urllib.parse import urlparse
import os
from src.models.query import Query
from src.models.response import Response
from src.models.staff_assignment import StaffAssignment
from src.models.query_event import QueryEvent

def save_response_file(db: Session, file: UploadFile,):
    upload_dir = "uploads/escalation_files"
    os.makedirs(upload_dir, exist_ok=True)

    safe_name = file.filename.replace(" ", "_")
    file_path = os.path.join(upload_dir, safe_name)

    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    attachment = Attachment(
        file_name=file.filename,
        file_url=file_path,
        file_type=file.filename.split(".")[-1],
        mime_type=file.content_type,
        # uploaded_by=uploaded_by,
    )

    db.add(attachment)
    db.commit()
    db.refresh(attachment)

    return attachment


def get_local_path_from_url(file_url: str):
    if not file_url:
        return None

    try:
        parsed = urlparse(file_url)
        return parsed.path.lstrip("/")  # uploads/documents/abc.pdf
    except:
        return None
    
    
def create_query_event(
    db: Session,
    query_id: int,
    event_type: str,
    event_message: str | None = None,
    created_by: int | None = None,
):
    event = QueryEvent(
        query_id=query_id,
        event_type=event_type,
        event_message=event_message,
        created_by=created_by,
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


def assign_query_to_staff(db: Session, query_id: int, assigned_to: int, assigned_by: int | None, notes: str | None = None):
    query_obj = db.query(Query).filter(Query.query_id == query_id).first()
    if not query_obj:
        return None

    query_obj.assigned_to = assigned_to
    query_obj.status = "assigned"   # keep this only if DB constraint allows it
    db.commit()
    
    assignment = StaffAssignment(
        query_id=query_obj.query_id,
        assigned_to=assigned_to,
        assigned_by=assigned_by,
        status="assigned",
        notes=notes,
    )
    db.add(assignment)

    event = QueryEvent(
        query_id=query_obj.query_id,
        event_type="assigned",
        event_message=f"Query assigned to staff id {assigned_to}",
        created_by=assigned_by,
    )
    db.add(event)

    try:
        db.commit()
        db.refresh(assignment)
        db.refresh(query_obj)
        #  GET STAFF
        staff = db.query(Users).filter(Users.user_id == assigned_to).first()

#  GET WHATSAPP NUMBER (IMPORTANT)
        whatsapp_number = None
        student = None 
# if stored in Query
        if hasattr(query_obj, "whatsapp_number"):
           whatsapp_number = query_obj.whatsapp_number

# fallback from student
        elif query_obj.student_user_id:
            student = db.query(Users).filter(
                Users.user_id == query_obj.student_user_id
            ).first()
            if student and hasattr(student, "phone"):
               whatsapp_number = student.phone
        
        return assignment
    except Exception:
        db.rollback()
        raise

def respond_to_escalated_query(
    db: Session,
    query_id: int,
    responder_id: int | None,
    response_text: str,
    attachment_id: int | None = None,
    file: UploadFile | None = None
):
    query_obj = db.query(Query).filter(Query.query_id == query_id).first()

    if not query_obj:
        return None
    
    attachment_path = None
    saved_attachment = None

# I MAKE THE CHANGES HERE: save uploaded file first
    if file:
        saved_attachment = save_response_file(
            db=db,
            file=file,
            # uploaded_by=responder_id,
        )
        attachment_id = saved_attachment.attachment_id
        attachment_path = saved_attachment.file_url
        
    response_row = Response(
        query_id=query_obj.query_id,
        response_text=response_text,
        response_type="manual",
        responder_id=responder_id,
        attachment_id=attachment_id,
    )

    db.add(response_row)

    query_obj.status = "resolved"
    query_obj.ai_response = response_text
    query_obj.resolution_type = "staff"
    query_obj.resolved_at = func.now()
    query_obj.updated_at = func.now()

    event = QueryEvent(
        query_id=query_obj.query_id,
        event_type="manual_response",
        event_message="Manual response submitted by staff/admin.",
        created_by=responder_id,
    )

    db.add(event)

    try:
        db.commit()
        db.refresh(response_row)
        db.refresh(query_obj)

        
        #  EMAIL LOGIC 
       
        student = None

        if query_obj.student_user_id:
            student = db.query(Users).filter(
                Users.user_id == query_obj.student_user_id
            ).first()

        # file_path = None

        if attachment_path is None and attachment_id:
            attachment = db.query(Attachment).filter(
                Attachment.attachment_id == attachment_id
            ).first()

            if attachment:
                attachment_path = get_local_path_from_url(attachment.file_url)

        # if student and student.email:
        #     send_email(
        #         to_email=student.email,
        #         subject="Response to your QueryMate query",
        #         body=response_text,
        #         attachment_path=attachment_path
        #     )

        

        return response_row

    except Exception as e:
        db.rollback()
        print("Respond query error:", e)
        raise


def mark_query_resolved(
    db: Session,
    query_id: int,
    responder_id: int | None = None,
    notes: str | None = None,
):
    query_obj = db.query(Query).filter(Query.query_id == query_id).first()
    if not query_obj:
        return None

    query_obj.status = "resolved"
    query_obj.resolved_at = func.now()
    query_obj.updated_at = func.now()

    db.commit()
    db.refresh(query_obj)

    create_query_event(
        db=db,
        query_id=query_id,
        event_type="resolved",
        event_message=notes or "Query marked as resolved.",
        created_by=responder_id,
    )

    return query_obj