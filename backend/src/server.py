"""
FastAPI Server Entry Point
Run this file to start the backend server.
"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.config.env import settings
from src.routes.auth_routes import router as auth_router
from src.routes.admin_routes import router as admin_router
from src.routes.kb_routes import router as kb_router
from src.routes.app_query_routes import router as app_query_router
from src.routes.whatsapp_routes import router as whatsapp_router

# Create FastAPI app
app = FastAPI(title="QueryMate Backend")

# Configure CORS properly
origins = settings.FRONTEND_ORIGINS if settings.FRONTEND_ORIGINS else ["http://localhost:3000", "http://127.0.0.1:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers - auth_router already has prefix="/auth" in the router definition
app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(kb_router)
app.include_router(app_query_router)
app.include_router(whatsapp_router)


@app.get("/")
def root():
    return {"status": "ok", "message": "QueryMate Backend is running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


# Run the server
if __name__ == "__main__":
    uvicorn.run(
        "src.server:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )

