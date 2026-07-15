import os
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from src.config.env import settings

SCOPES = ["https://www.googleapis.com/auth/drive"]


def get_drive_service():
    if not settings.GOOGLE_OAUTH_CLIENT_ID:
        raise ValueError("GOOGLE_OAUTH_CLIENT_ID is missing in .env")

    if not settings.GOOGLE_OAUTH_CLIENT_SECRET:
        raise ValueError("GOOGLE_OAUTH_CLIENT_SECRET is missing in .env")

    if not settings.GOOGLE_OAUTH_REFRESH_TOKEN:
        raise ValueError("GOOGLE_OAUTH_REFRESH_TOKEN is missing in .env")

    creds = Credentials(
        token=None,
        refresh_token=settings.GOOGLE_OAUTH_REFRESH_TOKEN,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=settings.GOOGLE_OAUTH_CLIENT_ID,
        client_secret=settings.GOOGLE_OAUTH_CLIENT_SECRET,
        scopes=SCOPES,
    )

    creds.refresh(Request())

    service = build("drive", "v3", credentials=creds)
    return service


def upload_file_to_drive(file_path: str, file_name: str):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    if not settings.GOOGLE_DRIVE_FOLDER_ID:
        raise ValueError("GOOGLE_DRIVE_FOLDER_ID is missing in .env")

    service = get_drive_service()

    file_metadata = {
        "name": file_name,
        "parents": [settings.GOOGLE_DRIVE_FOLDER_ID],
    }

    media = MediaFileUpload(file_path, resumable=False)

    created_file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields="id, webViewLink, webContentLink"
    ).execute()

    return {
        "file_id": created_file["id"],
        "file_url": created_file.get("webViewLink"),
        "download_url": created_file.get("webContentLink"),
    }