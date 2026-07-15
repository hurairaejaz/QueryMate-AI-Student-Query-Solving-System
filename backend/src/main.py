from fastapi import FastAPI
import os
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from src.config.env import settings
from src.routes.auth_routes import router as auth_router
from src.routes.admin_routes import router as admin_router
from src.routes.kb_routes import router as kb_router
from src.routes.app_query_routes import router as app_query_router
from src.routes.whatsapp_routes import router as whatsapp_router
from src.routes.test_drive_routes import router as test_drive_router
from src.routes.google_oauth_routes import router as google_oauth_router
from starlette.middleware.sessions import SessionMiddleware
from src.models.kb_content import KnowledgeBase
from src.models.attachements import Attachment
from src.routes.escalation_routes import router as admin_escalation_router
from src.routes.escalation_routes import router as escalation_router
from src.routes.notification_routes import router as notification_router
from src.routes.app_feedback_routes import router as app_feedback_router
from src.routes import profile_routes
from src.routes import public_routes
from src.routes import admin_dashboard_routes
from src.routes import admin_profile_routes
from src.routes.user import router as user_router
from huggingface_hub import login
import os

app = FastAPI(title="QueryMate Backend")

# Configure CORS properly
origins = settings.FRONTEND_ORIGINS if settings.FRONTEND_ORIGINS else ["http://localhost:3000", "http://127.0.0.1:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:3000", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SESSION_SECRET_KEY,
    same_site="lax",
    https_only=False,  # True after HTTPS deployment
)

os.makedirs("uploads/kb_files", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Include routers - auth_router already has prefix="/auth" defined in the router
app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(kb_router)
app.include_router(app_query_router)
app.include_router(whatsapp_router)
app.include_router(test_drive_router)
app.include_router(google_oauth_router)
app.include_router(escalation_router)
app.include_router(notification_router)
app.include_router(app_feedback_router)
app.include_router(profile_routes.router)
app.include_router(public_routes.router)
app.include_router(admin_dashboard_routes.router)
app.include_router(admin_profile_routes.router)
app.include_router(user_router)
@app.get("/")
def root():
    return {"status": "ok", "message": "QueryMate Backend is running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.on_event("startup")
def startup_event():
    token = os.getenv("HF_TOKEN")
    if token:
        login(token=token)

# Run the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )

