from datetime import datetime, timedelta, timezone
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
import smtplib
import re
from src.models.student_record import StudentRecord

from fastapi import HTTPException, Request
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy import or_
from sqlalchemy.orm import Session

from src.config.env import settings
from src.models.user import Users, AuthToken
from src.models.password_reset import PasswordResetOTP
from src.schemas.user import UserRegister
from src.utils.tokens import create_access_token, create_refresh_token
# from src.utils.security import hash_password 
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



def _now():
    return datetime.utcnow()


def _norm_email(email: str) -> str:
    return (email or "").strip().lower()


def _bcrypt_safe(password: str) -> str:
    return (password or "")[:72]


def hash_password(password: str) -> str:
    return pwd_context.hash(_bcrypt_safe(password))


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(_bcrypt_safe(plain_password), hashed_password)


def _allowed_admin_email(email: str) -> bool:
    return _norm_email(email) in settings.ADMIN_EMAILS



# Admin registration


def register_admin(db: Session, full_name: str, email: str, password: str):
    email_l = _norm_email(email)

    if not _allowed_admin_email(email_l):
        raise ValueError("This email is not allowed for admin registration.")

    existing = db.query(Users).filter(Users.email == email_l).first()
    if existing:
        raise ValueError("Admin already registered with this email.")

    user = Users(
        full_name=full_name.strip(),
        email=email_l,
        password_hash=hash_password(password),
        role="admin",
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    
    return user



#  login for admin + student


def login_user(db: Session, email: str, password: str):
    email_l = _norm_email(email)

    user = db.query(Users).filter(Users.email == email_l).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not user.password_hash:
        raise HTTPException(status_code=401, detail="Password not set for this account")
    #  Here i have make changes
    # if user.is_deleted:
    #   raise HTTPException(status_code=403, detail="Account deleted")
    if getattr(user, "is_deleted", False):
         raise ValueError("Account has been deleted")
    if not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access_token, access_exp = create_access_token(user.user_id, user.role)
    refresh_token, _ = create_refresh_token(user.user_id, user.role)

    db.add(
        AuthToken(
            user_id=user.user_id,
            access_token=access_token,
            refresh_token=refresh_token,
            expires_at=access_exp,
        )
    )

    user.last_login = _now()
    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "role": user.role,
        "user": {
            "user_id": user.user_id,
            "full_name": user.full_name,
            "email": user.email,
            "phone": user.phone,
            "role": user.role,
        },
    }


def login_admin(db: Session, email: str, password: str):
    result = login_user(db, email, password)

    if result["user"]["role"] not in ("admin", "superadmin"):
        raise HTTPException(status_code=403, detail="This account is not admin.")

    return result


def refresh_tokens(db: Session, user_id: int, role: str):
    access_token, access_exp = create_access_token(user_id, role)
    refresh_token, _ = create_refresh_token(user_id, role)

    db.add(
        AuthToken(
            user_id=user_id,
            access_token=access_token,
            refresh_token=refresh_token,
            expires_at=access_exp,
        )
    )
    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "role": role,
    }



# Student signup


def register_student(db: Session, full_name: str, phone: str, email: str, password: str, roll_number=None):

    email_l = _norm_email(email)

    if not email_l:
        raise HTTPException(status_code=400, detail="Email is required")

    # roll_number = (roll_number or "").strip()

    # if not roll_number:
    #     raise HTTPException(status_code=400, detail="Roll number is required")

    # student_record = db.query(StudentRecord).filter(
    # StudentRecord.roll_number == roll_number
    # ).first()
    
    # if not student_record:
    #   raise HTTPException(
    #     status_code=404,
    #     detail="Roll number not found in university records"
    # )
    
    #  3. Check duplicates
    if db.query(Users).filter(Users.email == email_l).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    if db.query(Users).filter(Users.phone == phone).first():
        raise HTTPException(status_code=400, detail="Phone already registered")

    # 4. Create user (NOT VERIFIED)
    user = Users(
        full_name=full_name.strip(),
        phone=phone.strip(),
        email=email_l,
        password_hash=hash_password(password),
        role="student",
        is_active=True
        
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return {
        "message": "User registered successfully",
        "user": {
            "user_id": user.user_id,
            "full_name": user.full_name,
            "phone": user.phone,
            "email": user.email,
            "role": user.role,
            "is_active": user.is_active,
        }
    }
    # 5. Send OTP
    # send_signup_otp(email_l, db)

    # return {
    #     "message": "OTP sent to your university email",
    #     "email": email_l
    # }
    
    
def register_user(db: Session, user_data: UserRegister):
    return register_student(
        db=db,
        full_name=user_data.full_name,
        phone=user_data.phone,
        email=user_data.email,
        password=user_data.password,
    )
  



# Password reset - Email based


def generate_otp() -> str:
    return str(random.randint(100000, 999999))


def find_user_by_identifier(db: Session, identifier: str):
    identifier = (identifier or "").strip()
    return db.query(Users).filter(
        or_(
            Users.email == identifier,
            Users.phone == identifier,
        )
    ).first()


def send_reset_otp(identifier: str, otp_code: str):
    print(f"[RESET PASSWORD OTP] Send to {identifier}: {otp_code}")


def create_password_reset_otp(db: Session, identifier: str):
    user = find_user_by_identifier(db, identifier)
    if not user:
        raise HTTPException(status_code=404, detail="User not registered")

    otp_code = generate_otp()
    expires_at = _now() + timedelta(minutes=10)

    reset_row = PasswordResetOTP(
        user_id=user.user_id,
        identifier=identifier,
        otp_code=otp_code,
        is_used=False,
        expires_at=expires_at,
    )

    db.add(reset_row)
    db.commit()
    db.refresh(reset_row)

    send_reset_otp(identifier, otp_code)

    return {
        "message": "OTP sent successfully",
        "identifier": identifier,
        "otp": otp_code,
    }


def reset_password_with_otp(db: Session, identifier: str, otp_code: str, new_password: str):
    user = find_user_by_identifier(db, identifier)
    if not user:
        raise HTTPException(status_code=404, detail="User not registered")

    otp_row = (
        db.query(PasswordResetOTP)
        .filter(
            PasswordResetOTP.identifier == identifier,
            PasswordResetOTP.otp_code == otp_code,
            PasswordResetOTP.is_used == False,
        )
        .order_by(PasswordResetOTP.created_at.desc())
        .first()
    )

    if not otp_row:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    if otp_row.expires_at < _now():
        raise HTTPException(status_code=400, detail="OTP expired")

    if len(new_password or "") < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters long")

    user.password_hash = hash_password(new_password)
    otp_row.is_used = True

    db.commit()

    return {"message": "Password updated successfully"}



# App forgot password - Phone based OTP


def send_forgot_password_otp(db: Session, phone: str):
    phone = (phone or "").strip()

    user = db.query(Users).filter(Users.phone == phone).first()

    if not user:
        raise HTTPException(status_code=404, detail="No account found with this phone number")

    otp = generate_otp()
    expiry = _now() + timedelta(minutes=5)

    user.otp_code = otp
    user.otp_expiry = expiry
    db.commit()

    return {
        "message": "OTP sent successfully",
        "otp": otp,  
    }


def verify_otp(db: Session, phone: str, otp: str):
    phone = (phone or "").strip()

    user = db.query(Users).filter(Users.phone == phone).first()

    if not user:
        raise HTTPException(status_code=404, detail="No account found with this phone number")

    if not user.otp_code or not user.otp_expiry:
        raise HTTPException(status_code=400, detail="No OTP found. Please request a new one.")

    if _now() > user.otp_expiry:
        raise HTTPException(status_code=400, detail="OTP has expired")

    if user.otp_code != otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    return {"message": "OTP verified successfully"}


def reset_password(db: Session, phone: str, otp: str, new_password: str):
    phone = (phone or "").strip()

    user = db.query(Users).filter(Users.phone == phone).first()

    if not user:
        raise HTTPException(status_code=404, detail="No account found with this phone number")

    if not user.otp_code or not user.otp_expiry:
        raise HTTPException(status_code=400, detail="No OTP found. Please request a new one.")

    if _now() > user.otp_expiry:
        raise HTTPException(status_code=400, detail="OTP has expired")

    if user.otp_code != otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    if len(new_password or "") < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters long")

    user.password_hash = hash_password(new_password)
    user.otp_code = None
    user.otp_expiry = None

    db.commit()

    return {"message": "Password reset successful"}



def create_password_reset_otp(db: Session, identifier: str):
    identifier = (identifier or "").strip()
    user = find_user_by_identifier(db, identifier)

    if not user:
        raise HTTPException(status_code=404, detail="User not registered")

    old_otps = (
        db.query(PasswordResetOTP)
        .filter(
            PasswordResetOTP.identifier == identifier,
            PasswordResetOTP.is_used == False,
        )
        .all()
    )

    for row in old_otps:
        row.is_used = True

    otp_code = generate_otp()
    expires_at = _now() + timedelta(minutes=10)

    reset_row = PasswordResetOTP(
        user_id=user.user_id,
        identifier=identifier,
        otp_code=otp_code,
        is_used=False,
        expires_at=expires_at,
    )

    db.add(reset_row)
    db.commit()
    db.refresh(reset_row)

    send_reset_otp(identifier, otp_code)

    return {
        "message": "OTP sent successfully",
        "identifier": identifier,
        "otp": otp_code,  
    }
    
    
def send_reset_otp(identifier: str, otp_code: str):
    
    if "@" not in identifier:
        print(f"[RESET PASSWORD OTP] Send to {identifier}: {otp_code}")
        return

    subject = "QueryMate Password Reset OTP"
    body = f"""
Hello,

Your QueryMate password reset OTP is: {otp_code}

This OTP will expire in 10 minutes.

If you did not request this, please ignore this email.

Regards,
QueryMate
"""

    msg = MIMEMultipart()
    msg["From"] = settings.SMTP_FROM
    msg["To"] = identifier
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT)
        server.starttls()
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.sendmail(settings.SMTP_FROM, identifier, msg.as_string())
        server.quit()
        print(f"[EMAIL SENT] OTP sent to {identifier}")
    except Exception as e:
        print(f"[EMAIL ERROR] {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to send email OTP: {str(e)}")    
    
def reset_password_with_otp(db: Session, identifier: str, otp_code: str, new_password: str):
    identifier = (identifier or "").strip()
    user = find_user_by_identifier(db, identifier)

    if not user:
        raise HTTPException(status_code=404, detail="User not registered")

    otp_row = (
        db.query(PasswordResetOTP)
        .filter(
            PasswordResetOTP.identifier == identifier,
            PasswordResetOTP.otp_code == otp_code,
            PasswordResetOTP.is_used == False,
        )
        .order_by(PasswordResetOTP.created_at.desc())
        .first()
    )

    if not otp_row:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    if otp_row.expires_at < _now():
        raise HTTPException(status_code=400, detail="OTP expired")

    if len((new_password or "").strip()) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters long")

    user.password_hash = hash_password(new_password.strip())
    otp_row.is_used = True

    db.commit()

    return {"message": "Password updated successfully"}   



def verify_reset_otp(db: Session, identifier: str, otp_code: str):
    user = find_user_by_identifier(db, identifier)
    if not user:
        raise HTTPException(status_code=404, detail="User not registered")

    otp_row = (
        db.query(PasswordResetOTP)
        .filter(
            PasswordResetOTP.identifier == identifier,
            PasswordResetOTP.otp_code == otp_code,
            PasswordResetOTP.is_used == False,
        )
        .order_by(PasswordResetOTP.created_at.desc())
        .first()
    )

    if not otp_row:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    if otp_row.expires_at < _now():
        raise HTTPException(status_code=400, detail="OTP expired")

    return {"message": "OTP verified successfully"}



def send_signup_otp(email, db):
    user = db.query(Users).filter(Users.email == email).first()

    if not user:
        raise Exception("User not found for OTP generation")

    otp = generate_otp()
    expires_at = _now() + timedelta(minutes=10)

    db_otp = PasswordResetOTP(
        user_id=user.user_id,
        identifier=email,
        otp_code=otp,
        is_used=False,
        expires_at=expires_at
    )

    db.add(db_otp)
    db.commit()
    
    
def verify_signup_otp(db: Session, email: str, otp_code: str):

    otp_row = (
        db.query(PasswordResetOTP)
        .filter(
            PasswordResetOTP.identifier == email,
            PasswordResetOTP.otp_code == otp_code,
            PasswordResetOTP.is_used == False,
        )
        .order_by(PasswordResetOTP.created_at.desc())
        .first()
    )

    if not otp_row:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    if otp_row.expires_at < _now():
        raise HTTPException(status_code=400, detail="OTP expired")

    user = db.query(Users).filter(Users.email == email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_active = True
    user.is_email_verified = True
    otp_row.is_used = True

    db.commit()

    return {"message": "Account verified successfully"}


def delete_user_account(db: Session, user_id: int):
    user = db.query(Users).filter(Users.user_id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    try:
        #  Delete related records first to avoid Foreign Key errors
        db.query(AuthToken).filter(AuthToken.user_id == user_id).delete()
        db.query(PasswordResetOTP).filter(PasswordResetOTP.user_id == user_id).delete()
        
        #  Delete the actual user record
        db.delete(user)
        db.commit()
        
        return {"message": "Account permanently deleted"}
    except Exception as e:
        db.rollback()
        print(f"Deletion Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error during deletion")