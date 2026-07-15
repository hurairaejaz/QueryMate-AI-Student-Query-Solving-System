import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[2]
ENV_PATH = BASE_DIR / ".env"
HF_LLM_MODEL: str = "HuggingFaceTB/SmolLM2-1.7B-Instruct"
MAX_NEW_TOKENS: int = 120
HF_EMBED_MODEL: str = "BAAI/bge-m3"
TOP_K: int = 5

print(f"[ENV] __file__: {__file__}")
print(f"[ENV] BASE_DIR: {BASE_DIR}")
print(f"[ENV] Looking for .env at: {ENV_PATH}")
print(f"[ENV] File exists: {ENV_PATH.exists()}")

load_dotenv(ENV_PATH, override=True)


class Settings:
    def __init__(self):
        self.DATABASE_URL: str = os.getenv("DATABASE_URL", "")
        if not self.DATABASE_URL:
           raise ValueError("DATABASE_URL is missing in .env")

        self.JWT_SECRET: str = os.getenv("JWT_SECRET", "change-me")
        self.JWT_ALG: str = os.getenv("JWT_ALG", "HS256")
        self.ACCESS_TOKEN_MINUTES: int = int(os.getenv("ACCESS_TOKEN_MINUTES", "60"))
        self.REFRESH_TOKEN_DAYS: int = int(os.getenv("REFRESH_TOKEN_DAYS", "30"))
        self.SESSION_SECRET_KEY: str = os.getenv("SESSION_SECRET_KEY", "change-this-secret")
        self.SMTP_HOST: str = os.getenv("SMTP_HOST", "smtp.gmail.com")
        self.SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
        self.SMTP_USER: str = os.getenv("SMTP_USER", "")
        self.SMTP_PASS: str = os.getenv("SMTP_PASS", "")
        self.SMTP_FROM: str = os.getenv("SMTP_FROM", "")

        self.GOOGLE_DRIVE_FOLDER_ID: str = os.getenv("GOOGLE_DRIVE_FOLDER_ID", "")
        self.GOOGLE_OAUTH_CLIENT_ID: str = os.getenv("GOOGLE_OAUTH_CLIENT_ID", "")
        self.GOOGLE_OAUTH_CLIENT_SECRET: str = os.getenv("GOOGLE_OAUTH_CLIENT_SECRET", "")
        self.GOOGLE_OAUTH_REDIRECT_URI: str = os.getenv("GOOGLE_OAUTH_REDIRECT_URI", "")
        self.GOOGLE_OAUTH_REFRESH_TOKEN: str = os.getenv("GOOGLE_OAUTH_REFRESH_TOKEN", "")

        self.ADMIN_EMAILS: list[str] = [
            e.strip().lower()
            for e in os.getenv("ADMIN_EMAILS", "").split(",")
            if e.strip()
        ]

        self.FRONTEND_ORIGINS: list[str] = [
            o.strip()
            for o in os.getenv(
                "FRONTEND_ORIGINS",
                "http://localhost:3000,http://127.0.0.1:3000",
            ).split(",")
            if o.strip()
        ]

        print(f"[ENV] DATABASE_URL loaded: {bool(self.DATABASE_URL)}")
        print(f"[ENV] GOOGLE_DRIVE_FOLDER_ID loaded: {bool(self.GOOGLE_DRIVE_FOLDER_ID)}")
        print(f"[ENV] GOOGLE_OAUTH_CLIENT_ID loaded: {bool(self.GOOGLE_OAUTH_CLIENT_ID)}")
        print(f"[ENV] GOOGLE_OAUTH_CLIENT_SECRET loaded: {bool(self.GOOGLE_OAUTH_CLIENT_SECRET)}")
        print(f"[ENV] GOOGLE_OAUTH_REDIRECT_URI: '{self.GOOGLE_OAUTH_REDIRECT_URI}'")
        print(f"[ENV] GOOGLE_OAUTH_REFRESH_TOKEN loaded: {bool(self.GOOGLE_OAUTH_REFRESH_TOKEN)}")
        print(f"[ENV] SESSION_SECRET_KEY loaded: {bool(self.SESSION_SECRET_KEY)}")

settings = Settings()