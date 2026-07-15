from fastapi import APIRouter, Depends, HTTPException, Response, Request, status
from sqlalchemy.orm import Session
from src.services.dependencies import get_current_user, get_current_user_from_cookie
from src.services.auth_services import verify_signup_otp
from src.config.database import get_db
from src.config.env import settings
from src.models.user import Users
from datetime import datetime
from src.utils.tokens import decode_token
from src.schemas.user import (
    AdminRegisterIn,
    AdminLoginIn,
    MeOut,
    UserRegister,
    UserLogin,
    RegisterResponse,
    ForgotPasswordRequest,
    ForgotPasswordResponse,
    ResetPasswordRequest,
    ResetPasswordResponse,
    ForgotPasswordIn,
    VerifyOtpIn,
    ResetPasswordIn,
)
from src.services.auth_services import (
    register_admin,
    login_admin,
    refresh_tokens,
    register_user,
    create_password_reset_otp,
    reset_password_with_otp,
    register_student,
    login_user,
    send_forgot_password_otp,
    verify_reset_otp,
    reset_password as reset_password_otp,
)
from src.utils.tokens import create_access_token, decode_token
from src.models.user import Users
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Define the security scheme
security = HTTPBearer()

router = APIRouter(prefix="/auth", tags=["Auth"])

COOKIE_COMMON = dict(
    httponly=True,
    samesite="Lax",
    secure=False,
    path="/",
)


# ADMIN ROUTES

@router.post("/admin/register", status_code=201)
def admin_register(payload: AdminRegisterIn, db: Session = Depends(get_db)):
    try:
        result = register_admin(db, payload.full_name, payload.email, payload.password)
        return {"message": "Admin registered", "user_id": result.user_id, "email": result.email, "role": result.role}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/admin/login")
def admin_login(payload: AdminLoginIn, response: Response, db: Session = Depends(get_db)):
    try:
        data = login_admin(
            db=db,
            email=payload.email,
            password=payload.password)  # Fixed: was 'pasword'
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

    response.set_cookie(
        key="access_token",
        value=data["access_token"],
        max_age=60 * settings.ACCESS_TOKEN_MINUTES,
        **COOKIE_COMMON
    )

    response.set_cookie(
        key="refresh_token",
        value=data["refresh_token"],
        max_age=60 * 60 * 24 * settings.REFRESH_TOKEN_DAYS,
        **COOKIE_COMMON
    )

    response.set_cookie(
        key="user_role",
        value=data["role"],
        max_age=60 * 60 * 24 * settings.REFRESH_TOKEN_DAYS,
        **{**COOKIE_COMMON, "httponly": False}
    )

    return {"message": "Login successful", "role": data["role"], "access_token": data["access_token"]}


# COMMON ROUTES

@router.post("/refresh")
def refresh(request: Request, response: Response, db: Session = Depends(get_db)):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Missing refresh token")

    try:
        payload = decode_token(refresh_token)
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    if payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid token type")

    user_id = int(payload.get("sub"))
    role = payload.get("role")

    data = refresh_tokens(db, user_id, role)

    response.set_cookie(key="access_token", value=data["access_token"], max_age=60 * settings.ACCESS_TOKEN_MINUTES, **COOKIE_COMMON)
    response.set_cookie(key="refresh_token", value=data["refresh_token"], max_age=60 * 60 * 24 * settings.REFRESH_TOKEN_DAYS, **COOKIE_COMMON)
    response.set_cookie(key="user_role", value=data["role"], max_age=60 * 60 * 24 * settings.REFRESH_TOKEN_DAYS, **{**COOKIE_COMMON, "httponly": False})

    return {"message": "Refreshed"}


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token", path="/")
    response.delete_cookie("refresh_token", path="/")
    response.delete_cookie("user_role", path="/")
    return {"message": "Logged out"}


@router.get("/me", response_model=MeOut)
def me(request: Request, db: Session = Depends(get_db)):
    from src.services.dependencies import get_current_user_from_cookie
    user_payload = get_current_user_from_cookie(request)
    user_id = int(user_payload.get("sub"))
    
    user = db.query(Users).filter(Users.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return MeOut(user_id=user.user_id, email=user.email, role=user.role, full_name=user.full_name)


# STUDENT AUTH ROUTES (for App)

@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
def register(payload: UserRegister, db: Session = Depends(get_db)):
    return register_student(
        db=db,
        full_name=payload.full_name,
        phone=payload.phone,
        email=payload.email,
        password=payload.password,
        # roll_number=payload.roll_number
    )

@router.post("/verify-signup-otp")
def verify_signup(email: str, otp: str, db: Session = Depends(get_db)):
    return verify_signup_otp(db, email, otp)


@router.post("/login")
def login(payload: UserLogin, db: Session = Depends(get_db)):
    return login_user(
        db=db,
        email=payload.email,
        password=payload.password,
    )


# PASSWORD RESET ROUTES (OTP to phone) 
@router.post("/forgot-password")
def forgot_password(payload: ForgotPasswordIn, db: Session = Depends(get_db)):
    return create_password_reset_otp(db, payload.identifier)


@router.post("/verify-otp")
def verify_otp_route(payload: VerifyOtpIn, db: Session = Depends(get_db)):
    return verify_reset_otp(db, payload.identifier, payload.otp_code) # pyright: ignore[reportUndefinedVariable]


@router.post("/reset-password")
def reset_password_route(payload: ResetPasswordIn, db: Session = Depends(get_db)):
    return reset_password_with_otp(
        db,
        payload.identifier,
        payload.otp_code,
        payload.new_password,
    )
    
    
    

@router.delete("/user/delete-account")
def delete_account(
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user)
):
    try:
        print("🔥 DELETE ROUTE HIT")

        print("USER:", current_user)

        user = db.query(Users).filter(
            Users.id == current_user.id
        ).first()

        print("DB USER:", user)

        if not user:
            return {"error": "User not found"}

        user.is_deleted = True
        user.deleted_at = datetime.utcnow()

        db.commit()

        return {"message": "Account deleted"}

    except Exception as e:
        db.rollback()
        print("🔥 FULL ERROR:", str(e))
        raise