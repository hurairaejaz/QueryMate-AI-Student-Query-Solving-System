from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session
from fastapi import Query
from src.config.database import get_db
from src.services.whatsapp_service import process_incoming_whatsapp_message
from src.services.whatsapp_service import handle_whatsapp_message
from typing import Dict, Any
router = APIRouter(prefix="/whatsapp", tags=["WhatsApp"])

VERIFY_TOKEN = "querymate_verify_token"



@router.get("/webhook")
def verify_webhook(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_verify_token: str = Query(None, alias="hub.verify_token"),
    hub_challenge: str = Query(None, alias="hub.challenge"),
):
    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN and hub_challenge:
        return PlainTextResponse(content=str(hub_challenge), status_code=200)

    raise HTTPException(status_code=403, detail="Webhook verification failed")


# @router.post("/webhook")
# async def receive_whatsapp_message(
#     request: Request,
#     db: Session = Depends(get_db),
# ):
#     payload = await request.json()

#     try:
#         entries = payload.get("entry", [])

#         for entry in entries:
#             changes = entry.get("changes", [])

#             for change in changes:
#                 value = change.get("value", {})

#                 contacts = value.get("contacts", [])
#                 messages = value.get("messages", [])

#                 profile_name = None
#                 if contacts:
#                     profile_name = contacts[0].get("profile", {}).get("name")

#                 for msg in messages:
#                     from_number = msg.get("from")
#                     msg_type = msg.get("type")

#                     if msg_type == "text":
#                         text_body = msg.get("text", {}).get("body", "").strip()

#                         if from_number and text_body:
#                             process_incoming_whatsapp_message(
#                                 db=db,
#                                 phone_number=from_number,
#                                 message_text=text_body,
#                                 profile_name=profile_name,
#                             )

#         return {"status": "received"}
@router.post("/webhook", operation_id="receive_whatsapp_message")
async def receive_whatsapp_message(
    payload: Dict[str, Any],
    db: Session = Depends(get_db),
):
    try:
        return handle_whatsapp_message(db=db, payload=payload)

    except Exception as e:
        print("WhatsApp webhook error:", e)
        raise HTTPException(
            status_code=500,
            detail=f"Webhook processing failed: {str(e)}",
        )
        
    except Exception as e:
        print("WhatsApp webhook error:", e)
        raise HTTPException(
            status_code=500,
            detail=f"Webhook processing failed: {str(e)}",
        )