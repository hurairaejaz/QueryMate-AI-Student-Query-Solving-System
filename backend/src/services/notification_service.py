
# import os
# from sqlalchemy.orm import Session

# from src.models.attachements import Attachment
# from src.models.notification import Notification
# from src.models.user import Users
# from src.models.query import Query
# from src.services.email_service import send_email
# from src.services.whatsapp_service import send_whatsapp_message

# _sent_notifications = set()

# def already_sent(key: str):
#     return key in _sent_notifications

# def mark_sent(key: str):
#     _sent_notifications.add(key)
    
    

# def create_app_notification(
#     db: Session,
#     user_id: int,
#     query_id: int | None,
#     title: str,
#     message: str,
#     notification_type: str,
# ):
#     notification = Notification(
#         user_id=user_id,
#         query_id=query_id,
#         title=title,
#         message=message,
#         type=notification_type,
#         is_read=False,
#     )

#     db.add(notification)
#     db.commit()
#     db.refresh(notification)

#     return notification


# def _get_attachment_path(db: Session, query_obj: Query):
#     if not query_obj:
#         return None

#     attachment = None

    
#     # First check latest manual response attachment.
#     if query_obj.responses:
#         latest_response = query_obj.responses[-1]

#         if latest_response.attachment_id:
#             attachment = db.query(Attachment).filter(
#                 Attachment.attachment_id == latest_response.attachment_id
#             ).first()

   
#     # If no response attachment, then check matched KB attachment.
#     if not attachment:
#         attachment = getattr(query_obj, "matched_attachment", None)

#     if not attachment or not attachment.file_url:
#         return None

#     file_path = attachment.file_url

#     if file_path.startswith("http"):
#         if "uploads/" in file_path:
#             file_path = file_path.split("uploads/")[-1]
#             file_path = os.path.join("uploads", file_path)
#         else:
#             return None

#     file_path = file_path.replace("\\", os.sep).replace("/", os.sep)

#     if os.path.exists(file_path):
#         return file_path

#     print("Attachment file not found:", file_path)
#     return None


# def notify_query_assigned(
#     db: Session,
#     query_obj: Query,
#     assigned_staff_email: str | None = None,
#     assigned_staff_name: str | None = None,
# ):
#     key = f"assigned_{query_obj.query_id}"

# #   Prevent duplicate email execution
#     if already_sent(key):
#         return True

#     mark_sent(key)
#     if not query_obj:
#             return False

#     student = None

#     if query_obj.student_user_id:
#         student = db.query(Users).filter(
#             Users.user_id == query_obj.student_user_id
#         ).first()

#     # Get WhatsApp number from query (for WhatsApp-based queries)
#     whatsapp_number = None
#     if query_obj.source == "whatsapp" and query_obj.whatsapp_user:
#         whatsapp_number = query_obj.whatsapp_user.phone_number

#     final_staff_name = assigned_staff_name or "Staff Member"
#     final_staff_email = assigned_staff_email

#     # student notification + email
#     if student:
#         create_app_notification(
#             db=db,
#             user_id=student.user_id,
#             query_id=query_obj.query_id,
#             title="Your query has been assigned",
#             message=(
#                 "Your query has been assigned.\n\n"
#                 f"Assigned Staff: {final_staff_name}\n\n"
#                 f"Query:\n{query_obj.query_text}"
#             ),
#             notification_type="assigned",
#         )

#         if student.email:
#             send_email(
#                 to_email=student.email,
#                 subject="QueryMate - Your query has been assigned",
#                 body=f"""
# Hello {student.full_name},

# Your query has been assigned to:

# Staff Name:
# {final_staff_name}

# Staff Email:
# {final_staff_email or "N/A"}

# Query:
# {query_obj.query_text}

# Regards,
# QueryMate Team
# """
#             )
#     # WhatsApp notification
    
#     if whatsapp_number:
#         send_whatsapp_message(
#             to=whatsapp_number,
#             message=f"""
# 📌 Query Assigned

# ID: {query_obj.query_id}

# Query:
# {query_obj.query_text}

# Assigned To: {final_staff_name}

# Status: Pending
# """
#         )
        
        
#     # selected staff email
#     staff_email_sent = False

#     if final_staff_email:
#         staff_email_sent = send_email(
#             to_email=final_staff_email,
#             subject="QueryMate - New Query Assigned to You",
#             body=f"""
# Hello {final_staff_name},

# A new student query has been assigned to you.

# Query ID:
# {query_obj.query_id}

# Student:
# {student.full_name if student else "N/A"}

# Student Email:
# {student.email if student else "N/A"}


# Student WhatsApp Number:
# {whatsapp_number if whatsapp_number else "N/A"}

# Query:
# {query_obj.query_text}

# Please respond As Soon As possible.

# Regards,
# QueryMate System
# """
#         )

#     print("Assigned staff name:", final_staff_name)
#     print("Assigned staff email:", final_staff_email)
#     print("Staff email sent:", staff_email_sent)

#     return True


# def notify_query_answered(db: Session, query_obj: Query):
#     if not query_obj or not query_obj.student_user_id:
#         return False

#     create_app_notification(
#         db=db,
#         user_id=query_obj.student_user_id,
#         query_id=query_obj.query_id,
#         title="Query Answered",
#         message=f"""
# Your query has been answered successfully.

# Query:
# {query_obj.query_text}
#         """,
#         notification_type="query_answered",
#     )

#     return True


# def notify_query_resolved(
#     db: Session,
#     query_obj: Query,
#     response_text: str | None = None,
# ):
#     key = f"resolved_{query_obj.query_id}"

# #  Prevent duplicate email execution
#     if already_sent(key):
#         return True

#     mark_sent(key)
    
#     if not query_obj:
#         return False

#     if not query_obj.student_user_id:
#         print("NO STUDENT USER ID FOUND FOR QUERY:", query_obj.query_id)
#         return False

#     student = db.query(Users).filter(
#         Users.user_id == query_obj.student_user_id
#     ).first()

#     if not student:
#         print("NO STUDENT FOUND FOR USER ID:", query_obj.student_user_id)
#         return False

#     final_response = response_text or "Your query has been answered by admin."
    
#     create_app_notification(
#         db=db,
#         user_id=student.user_id,
#         query_id=query_obj.query_id,
#         title="""Your query has been answered
        
#         Please check your email for full details.
#         """,
#         message=f"""
#         Query:
#         {query_obj.query_text}
#         Admin Response:
#         {final_response}
#         """,
#               notification_type="query_answered",
#     )

#     attachment_path = _get_attachment_path(db, query_obj)

#     email_sent = False

#     if student.email:
#         email_sent = send_email(
#             to_email=student.email,
#             subject="QueryMate - Your query has been answered",
#             body=f"""
# Hello {student.full_name},

# Your query has been answered.

# Query:
# {query_obj.query_text}

# Response:
# {final_response}

# Regards,
# QueryMate Team
# """,
#             attachment_path=attachment_path,
#         )
        
#     if getattr(student, "phone_number", None):
#         send_whatsapp_message(
#             to=student.phone_number,
#             message=f"""
# Query Resolved

# ID: {query_obj.query_id}

# Query:
# {query_obj.query_text}

# Response:
# {final_response}

# Status: Resolved
# """
#         )

#     return True

#     print("Notification created for:", student.email)
#     print("Attachment path:", attachment_path)
#     print("Email sent:", email_sent)

#     return True


# def send_query_answer_email(user_email: str, subject: str, body: str):
#     if not user_email:
#         return False

#     try:
#         send_email(
#             to_email=user_email,
#             subject=subject,
#             body=body,
#         )
#         return True

#     except Exception as e:
#         print("Email send failed:", e)
#         return False


import os
from sqlalchemy.orm import Session

from src.models.attachements import Attachment
from src.models.notification import Notification
from src.models.user import Users
from src.models.query import Query
from src.services.email_service import send_email
from src.services.whatsapp_service import send_whatsapp_message


_sent_notifications = set()

def already_sent(key: str):
    return key in _sent_notifications


def mark_sent(key: str):
    _sent_notifications.add(key)


def create_app_notification(
    db: Session,
    user_id: int,
    query_id: int | None,
    title: str,
    message: str,
    notification_type: str,
):
    notification = Notification(
        user_id=user_id,
        query_id=query_id,
        title=title,
        message=message,
        type=notification_type,
        is_read=False,
    )

    db.add(notification)
    db.commit()
    db.refresh(notification)

    return notification


def _get_attachment_path(db: Session, query_obj: Query):
    if not query_obj:
        return None

    attachment = None

    # First check latest manual response attachment.
    if query_obj.responses:
        latest_response = query_obj.responses[-1]

        if latest_response.attachment_id:
            attachment = db.query(Attachment).filter(
                Attachment.attachment_id == latest_response.attachment_id
            ).first()

    # If no response attachment, then check matched KB attachment.
    if not attachment:
        attachment = getattr(query_obj, "matched_attachment", None)

    if not attachment or not attachment.file_url:
        return None

    file_path = attachment.file_url

    if file_path.startswith("http"):
        if "uploads/" in file_path:
            file_path = file_path.split("uploads/")[-1]
            file_path = os.path.join("uploads", file_path)
        else:
            return None

    file_path = file_path.replace("\\", os.sep).replace("/", os.sep)

    if os.path.exists(file_path):
        return file_path

    print("Attachment file not found:", file_path)
    return None


def notify_query_assigned(
    db: Session,
    query_obj: Query,
    assigned_staff_email: str | None = None,
    assigned_staff_name: str | None = None,
):
    key = f"assigned_{query_obj.query_id}"

    # Prevent duplicate email execution
    if already_sent(key):
        return True

    mark_sent(key)

    if not query_obj:
        return False

    student = None

    if query_obj.student_user_id:
        student = db.query(Users).filter(
            Users.user_id == query_obj.student_user_id
        ).first()

    # Get WhatsApp number from query (for WhatsApp-based queries)
    whatsapp_number = None
    if query_obj.source == "whatsapp" and query_obj.whatsapp_user:
        whatsapp_number = query_obj.whatsapp_user.phone_number

    final_staff_name = assigned_staff_name or "Staff Member"
    final_staff_email = assigned_staff_email

    # student notification + email
    if student:
        create_app_notification(
            db=db,
            user_id=student.user_id,
            query_id=query_obj.query_id,
            title="Your query has been assigned",
            message=(
                "Your query has been assigned.\n\n"
                f"Query:\n{query_obj.query_text}\n\n"
                f"Assigned Staff: {final_staff_name}\n\n"
                f"Staff Email:{final_staff_email or "N/A"}"
            ),
            notification_type="assigned",
        )

        if student.email:
            send_email(
                to_email=student.email,
                subject="QueryMate - Your query has been assigned",
                body=f"""
Hello {student.full_name},

Your query has been assigned to:

Staff Name:
{final_staff_name}

Staff Email:
{final_staff_email or "N/A"}

Query:
{query_obj.query_text}

Regards,
QueryMate Team
"""
            )

    # WhatsApp notification
    if whatsapp_number:
        send_whatsapp_message(
            to=whatsapp_number,
            message=f"""
Query Assigned

ID: {query_obj.query_id}

Query:
{query_obj.query_text}

Assigned To: {final_staff_name}

Status: Pending
"""
        )

    # selected staff email
    staff_email_sent = False

    if final_staff_email:
        staff_email_sent = send_email(
            to_email=final_staff_email,
            subject="QueryMate - New Query Assigned to You",
            body=f"""
Hello {final_staff_name},

A new student query has been assigned to you.

Query ID:
{query_obj.query_id}

Student:
{student.full_name if student else "N/A"}

Student Email:
{student.email if student else "N/A"}

Student WhatsApp Number:
{whatsapp_number if whatsapp_number else "N/A"}

Query:
{query_obj.query_text}

Please respond As Soon As possible.

Regards,
QueryMate System
"""
        )

    print("Assigned staff name:", final_staff_name)
    print("Assigned staff email:", final_staff_email)
    print("Staff email sent:", staff_email_sent)

    return True


def notify_query_answered(db: Session, query_obj: Query):
    if not query_obj or not query_obj.student_user_id:
        return False

    create_app_notification(
        db=db,
        user_id=query_obj.student_user_id,
        query_id=query_obj.query_id,
        title="Query Answered",
        message=f"""
Your query has been answered successfully.

Query:
{query_obj.query_text}
        """,
        notification_type="query_answered",
    )

    return True


def notify_query_resolved(
    db: Session,
    query_obj: Query,
    response_text: str | None = None,
):
    key = f"resolved_{query_obj.query_id}"

    # Prevent duplicate email execution
    if already_sent(key):
        return True

    mark_sent(key)

    if not query_obj:
        return False

    if not query_obj.student_user_id:
        print("NO STUDENT USER ID FOUND FOR QUERY:", query_obj.query_id)
        return False

    student = db.query(Users).filter(
        Users.user_id == query_obj.student_user_id
    ).first()

    if not student:
        print("NO STUDENT FOUND FOR USER ID:", query_obj.student_user_id)
        return False

    final_response = response_text or "Your query has been answered by admin."

    create_app_notification(
        db=db,
        user_id=student.user_id,
        query_id=query_obj.query_id,
        title="""Your query has been answered
        
        Please check your email for full details.
        """,
        message=f"""
        Query:
        {query_obj.query_text}
        Admin Response:
        {final_response}
        """,
        notification_type="query_answered",
    )

    attachment_path = _get_attachment_path(db, query_obj)

    email_sent = False

    if student.email:
        email_sent = send_email(
            to_email=student.email,
            subject="QueryMate - Your query has been answered",
            body=f"""
Hello {student.full_name},

Your query has been answered.

Query:
{query_obj.query_text}

Response:
{final_response}

Regards,
QueryMate Team
""",
            attachment_path=attachment_path,
        )

    if getattr(student, "phone_number", None):
        send_whatsapp_message(
            to=student.phone_number,
            message=f"""
Query Resolved



Query:
{query_obj.query_text}

Response:
{final_response}

Status: Resolved
"""
        )

    print("Notification created for:", student.email)
    print("Attachment path:", attachment_path)
    print("Email sent:", email_sent)

    return True


def send_query_answer_email(user_email: str, subject: str, body: str):
    if not user_email:
        return False

    try:
        send_email(
            to_email=user_email,
            subject=subject,
            body=body,
        )
        return True

    except Exception as e:
        print("Email send failed:", e)
        return False