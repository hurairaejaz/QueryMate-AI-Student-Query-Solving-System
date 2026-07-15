from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from src.config.env import settings

engine = create_engine(settings.DATABASE_URL, echo=False)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    from src.models.user import Users, AuthToken, Departments, Feedback, ActivityLogs
    from src.models.password_reset import PasswordResetOTP
    from src.models.kb_content import KnowledgeBase, KbCategory
    from src.models.query import Query
    from src.models.response import Response
    from src.models.whatsapp_user import WhatsAppUsers
    from src.models.whatsapp_message import WhatsAppMessages
    from src.models.attachements import Attachment

    Base.metadata.create_all(bind=engine)