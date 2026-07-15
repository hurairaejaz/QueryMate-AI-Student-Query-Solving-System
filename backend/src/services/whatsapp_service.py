import requests
from sqlalchemy.orm import Session
import os
from urllib.parse import urlparse

from src.models.whatsapp_user import WhatsAppUsers
from src.models.whatsapp_message import WhatsAppMessages
from src.services.query_service import submit_whatsapp_query


WHATSAPP_API_URL = "https://graph.facebook.com/v25.0"

WHATSAPP_PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
WHATSAPP_ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN")


def get_or_create_whatsapp_user(db: Session, phone_number: str, profile_name: str | None = None):
    user = (
        db.query(WhatsAppUsers)
        .filter(WhatsAppUsers.phone_number == phone_number)
        .first()
    )

    if user:
        return user

    user = WhatsAppUsers(
        phone_number=phone_number,
        name=profile_name or phone_number,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def save_whatsapp_message(
    db: Session,
    whatsapp_user_id: int,
    query_id: int | None,
    direction: str,
    message_type: str,
    message_text: str | None = None,
    media_url: str | None = None,
    meta_message_id: str | None = None,
):
    msg = WhatsAppMessages(
        whatsapp_user_id=whatsapp_user_id,
        query_id=query_id,
        direction=direction,
        message_type=message_type,
        message_text=message_text,
        media_url=media_url,
        meta_message_id=meta_message_id,
    )

    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg


def send_whatsapp_text(to_number: str, message: str):
    url = f"{WHATSAPP_API_URL}/{WHATSAPP_PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {WHATSAPP_ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "text",
        "text": {"body": message},
    }

    response = requests.post(url, headers=headers, json=payload, timeout=30)

    print("WhatsApp text send:", response.status_code, response.text)

    if response.status_code not in [200, 201]:
        print("WhatsApp send text failed:", response.status_code, response.text)

    return response.status_code, response.text


def convert_file_url_to_path(file_url: str) -> str:
    file_url = (file_url or "").strip()
    parsed = urlparse(file_url)

    if parsed.scheme in ["http", "https"]:
        file_path = parsed.path.lstrip("/")
    else:
        file_path = file_url.lstrip("/")

    return os.path.normpath(file_path)


def upload_whatsapp_media(file_path: str, mime_type: str):
    url = f"{WHATSAPP_API_URL}/{WHATSAPP_PHONE_NUMBER_ID}/media"

    headers = {
        "Authorization": f"Bearer {WHATSAPP_ACCESS_TOKEN}",
    }

    with open(file_path, "rb") as file:
        files = {
            "file": (
                os.path.basename(file_path),
                file,
                mime_type or "application/octet-stream",
            )
        }

        data = {
            "messaging_product": "whatsapp",
            "type": mime_type or "application/octet-stream",
        }

        response = requests.post(
            url,
            headers=headers,
            files=files,
            data=data,
            timeout=60,
        )

    print("WhatsApp media upload:", response.status_code, response.text)

    if response.status_code not in [200, 201]:
        raise Exception(f"WhatsApp media upload failed: {response.text}")

    return response.json()["id"]


def send_whatsapp_document(
    to_number: str,
    media_id: str,
    file_name: str,
    caption: str | None = None,
):
    url = f"{WHATSAPP_API_URL}/{WHATSAPP_PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {WHATSAPP_ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }

    document_payload = {
        "id": media_id,
        "filename": file_name,
    }

    if caption:
        document_payload["caption"] = caption[:1000]

    payload = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "document",
        "document": document_payload,
    }

    response = requests.post(url, headers=headers, json=payload, timeout=30)

    print("WhatsApp document send:", response.status_code, response.text)

    if response.status_code not in [200, 201]:
        print("WhatsApp send document failed:", response.status_code, response.text)

    return response.status_code, response.text


def handle_whatsapp_message(db: Session, payload: dict):
    print("WHATSAPP WEBHOOK HIT")
    print("PAYLOAD:", payload)

    entries = payload.get("entry", [])

    for entry in entries:
        changes = entry.get("changes", [])

        for change in changes:
            value = change.get("value", {})
            contacts = value.get("contacts", [])
            messages = value.get("messages", [])

            profile_name = None
            if contacts:
                profile_name = contacts[0].get("profile", {}).get("name")

            for msg in messages:
                from_number = msg.get("from")
                msg_type = msg.get("type")
                whatsapp_message_id = msg.get("id")

                if msg_type == "text":
                    text_body = msg.get("text", {}).get("body", "").strip()

                    if from_number and text_body:
                        process_incoming_whatsapp_message(
                            db=db,
                            phone_number=from_number,
                            message_text=text_body,
                            profile_name=profile_name,
                            whatsapp_message_id=whatsapp_message_id,
                        )

    return {"status": "received"}


def process_incoming_whatsapp_message(
    db: Session,
    phone_number: str,
    message_text: str,
    profile_name: str | None = None,
    whatsapp_message_id: str | None = None,
):
    whatsapp_user = get_or_create_whatsapp_user(
        db=db,
        phone_number=phone_number,
        profile_name=profile_name,
    )

    # STOP duplicate webhook retry from Meta
    if whatsapp_message_id:
        existing_msg = (
            db.query(WhatsAppMessages)
            .filter(WhatsAppMessages.meta_message_id == whatsapp_message_id)
            .first()
        )

        if existing_msg:
            print("Duplicate WhatsApp message ignored:", whatsapp_message_id)
            return {"status": "duplicate_ignored"}

    save_whatsapp_message(
        db=db,
        whatsapp_user_id=whatsapp_user.whatsapp_user_id,
        query_id=None,
        direction="inbound",
        message_type="text",
        message_text=message_text,
        meta_message_id=whatsapp_message_id,
    )

    result = submit_whatsapp_query(
        db=db,
        whatsapp_user_id=whatsapp_user.whatsapp_user_id,
        query_text=message_text,
    )

    query_id = result.get("query_id")
    answer_text = (result.get("answer") or "").strip()
    documents = result.get("documents") or []
    to_number = whatsapp_user.phone_number

    has_answer = bool(answer_text)
    has_document = bool(documents)

    # Answer exists, with or without document
    if has_answer:
        send_whatsapp_text(to_number, answer_text)

        save_whatsapp_message(
            db=db,
            whatsapp_user_id=whatsapp_user.whatsapp_user_id,
            query_id=query_id,
            direction="outbound",
            message_type="text",
            message_text=answer_text,
        )

        if has_document:
            first_doc = documents[0]

            doc_url = (
                first_doc.get("file_url")
                or first_doc.get("download_url")
                or first_doc.get("open_url")
            )

            file_name = first_doc.get("file_name") or "document"
            mime_type = first_doc.get("mime_type") or "application/octet-stream"

            if doc_url:
                try:
                    file_path = convert_file_url_to_path(doc_url)

                    if not os.path.exists(file_path):
                        raise Exception(f"Document file not found on server: {file_path}")

                    media_id = upload_whatsapp_media(
                        file_path=file_path,
                        mime_type=mime_type,
                    )

                    send_whatsapp_document(
                        to_number=to_number,
                        media_id=media_id,
                        file_name=file_name,
                        caption="Please find the attached document.",
                    )

                    save_whatsapp_message(
                        db=db,
                        whatsapp_user_id=whatsapp_user.whatsapp_user_id,
                        query_id=query_id,
                        direction="outbound",
                        message_type="document",
                        message_text=file_name,
                        media_url=media_id,
                    )

                except Exception as e:
                    print("WhatsApp document attachment error:", e)

                    fallback_doc_link = doc_url

                    if fallback_doc_link.startswith("/"):
                        fallback_doc_link = (
                            f"https://leverage-glazing-unheated.ngrok-free.dev"
                            f"{fallback_doc_link}"
                        )

                    send_whatsapp_text(
                        to_number,
                        f"Document could not be attached directly. Please open it here:\n{fallback_doc_link}",
                    )

                    save_whatsapp_message(
                        db=db,
                        whatsapp_user_id=whatsapp_user.whatsapp_user_id,
                        query_id=query_id,
                        direction="outbound",
                        message_type="document_link_fallback",
                        message_text=fallback_doc_link,
                        media_url=fallback_doc_link,
                    )

        return result

    #  No answer but document exists
    if has_document:
        send_whatsapp_text(
            to_number,
            "I found a relevant document for your query. Please check the attached file.",
        )

        first_doc = documents[0]

        doc_url = (
            first_doc.get("file_url")
            or first_doc.get("download_url")
            or first_doc.get("open_url")
        )

        file_name = first_doc.get("file_name") or "document"
        mime_type = first_doc.get("mime_type") or "application/octet-stream"

        if doc_url:
            try:
                file_path = convert_file_url_to_path(doc_url)

                if not os.path.exists(file_path):
                    raise Exception(f"Document file not found on server: {file_path}")

                media_id = upload_whatsapp_media(
                    file_path=file_path,
                    mime_type=mime_type,
                )

                send_whatsapp_document(
                    to_number=to_number,
                    media_id=media_id,
                    file_name=file_name,
                    caption="Please find the attached document.",
                )

                save_whatsapp_message(
                    db=db,
                    whatsapp_user_id=whatsapp_user.whatsapp_user_id,
                    query_id=query_id,
                    direction="outbound",
                    message_type="document",
                    message_text=file_name,
                    media_url=media_id,
                )

            except Exception as e:
                print("WhatsApp document attachment error:", e)

                fallback_doc_link = doc_url

                if fallback_doc_link.startswith("/"):
                    fallback_doc_link = (
                        f"https://leverage-glazing-unheated.ngrok-free.dev"
                        f"{fallback_doc_link}"
                    )

                send_whatsapp_text(
                    to_number,
                    f"Document could not be attached directly. Please open it here:\n{fallback_doc_link}",
                )

                save_whatsapp_message(
                    db=db,
                    whatsapp_user_id=whatsapp_user.whatsapp_user_id,
                    query_id=query_id,
                    direction="outbound",
                    message_type="document_link_fallback",
                    message_text=fallback_doc_link,
                    media_url=fallback_doc_link,
                )

        return result

    # No answer and no document 
    escalation_message = (
        "Unfortunately, our database does not have a reliable answer to your question at that moment. Your query has been escalated to our support team, and they will get back to you as soon as possible. We apologize for the inconvenience. Thank you for your understanding.❤️"
    )

    send_whatsapp_text(to_number, escalation_message)

    save_whatsapp_message(
        db=db,
        whatsapp_user_id=whatsapp_user.whatsapp_user_id,
        query_id=query_id,
        direction="outbound",
        message_type="status",
        message_text=escalation_message,
    )

    return result

def send_whatsapp_message(to: str, message: str):
    return send_whatsapp_text(to, message)
