from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse
from google_auth_oauthlib.flow import Flow
from src.config.env import settings

router = APIRouter(tags=["Google OAuth"])

SCOPES = ["https://www.googleapis.com/auth/drive"]


def build_flow(state: str | None = None, code_verifier: str | None = None):
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": settings.GOOGLE_OAUTH_CLIENT_ID,
                "client_secret": settings.GOOGLE_OAUTH_CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [settings.GOOGLE_OAUTH_REDIRECT_URI],
            }
        },
        scopes=SCOPES,
        state=state,
    )

    flow.redirect_uri = settings.GOOGLE_OAUTH_REDIRECT_URI

    if code_verifier:
        flow.code_verifier = code_verifier

    return flow


@router.get("/google/login")
def google_login(request: Request):
    flow = build_flow()

    auth_url, state = flow.authorization_url(
        access_type="offline",
        prompt="consent",
        include_granted_scopes="true",
    )

    request.session["google_oauth_state"] = state
    request.session["google_code_verifier"] = flow.code_verifier

    print("LOGIN STATE SAVED:", state)
    print("LOGIN CODE VERIFIER SAVED:", flow.code_verifier)

    return RedirectResponse(auth_url)


@router.get("/google/callback")
def google_callback(request: Request, code: str, state: str):
    saved_state = request.session.get("google_oauth_state")
    saved_code_verifier = request.session.get("google_code_verifier")

    print("CALLBACK RECEIVED STATE:", state)
    print("SESSION SAVED STATE:", saved_state)
    print("SESSION SAVED CODE VERIFIER:", saved_code_verifier)

    if not saved_state:
        raise HTTPException(status_code=400, detail="OAuth state missing from session")

    if not saved_code_verifier:
        raise HTTPException(status_code=400, detail="OAuth code verifier missing from session")

    if state != saved_state:
        raise HTTPException(status_code=400, detail="OAuth state mismatch")

    flow = build_flow(state=saved_state, code_verifier=saved_code_verifier)
    flow.fetch_token(code=code)

    creds = flow.credentials

    request.session.pop("google_oauth_state", None)
    request.session.pop("google_code_verifier", None)

    return {
        "message": "Copy this refresh token into your .env",
        "refresh_token": creds.refresh_token,
        "access_token": creds.token
    }