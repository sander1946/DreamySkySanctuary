import io
from typing import Annotated

from fastapi import APIRouter, Depends, Form, HTTPException, Request, Security, status
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException, InsufficientScopeException

import pyotp
from werkzeug.security import generate_password_hash, check_password_hash

from src.utils.flash import get_flashed_messages, flash
from src.config import config
from src.schemas.Login import LoginForm, RegisterForm, Scopes, User, UserDB, UserRequestSchema
from src.utils.database import close_connection, create_connection, create_user, get_user_by_username, update_otp_user

import qrcode

login_manager = LoginManager(config.SERVER_SECRET, token_url="/auth/login", use_cookie=True)
login_manager.cookie_name = "user_token"

templates = Jinja2Templates(directory=config.TEMPLATES_DIR)
templates.env.globals["get_flashed_messages"] = get_flashed_messages

router = APIRouter(
    prefix="",
    tags=["Authentication"],
)


def get_user_access_cookie(user: UserDB):
    scopes = [Scopes.BASIC.value if not user.is_admin else Scopes.ADMIN.value]
    if not user.otp_enabled:
        scopes.append(Scopes.OTP_CHECKED.value)
    
    access_token = login_manager.create_access_token(
        data={"sub": user.username},
        expires=config.ACCESS_TOKEN_EXPIRE_MINUTES,
        scopes=scopes,
    )
    return access_token


@login_manager.user_loader()
def load_user(username: str) -> UserDB:
    connection = create_connection("Website")
    user = get_user_by_username(connection, username)
    close_connection(connection)
    return user


def check_user_password(user: UserDB, plain_password: str) -> bool:
    return check_password_hash(user.password_hash, plain_password)


@router.get("/register")
def register_page(request: Request):
    return templates.TemplateResponse("auth/register.html", {"request": request})


@router.post("/auth/register")
def register(request: Request, register_data: Annotated[RegisterForm, Form()]):
    username = register_data.username
    email = register_data.email
    password = register_data.password
    password_hash = generate_password_hash(password)
    
    connection = create_connection("Website")
    user = get_user_by_username(connection, username)
    
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
    
    userDB = UserDB(username=username, email=email, password_hash=password_hash)
    
    create_user(connection, userDB)
    close_connection(connection)
    
    response = RedirectResponse(url="/account", status_code=status.HTTP_302_FOUND)
    login_manager.set_cookie(response, get_user_access_cookie(userDB))
    return response


@router.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})


@router.post("/auth/login")
def login(request: Request, login_data: Annotated[LoginForm, Form()]):
    username = login_data.username
    password = login_data.password
    
    user: UserDB = load_user(username)
    
    if not user:
        flash(request, "The username or password is incorrect", "warning")
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    
    if not check_user_password(user, password):
        flash(request, "The username or password is incorrect", "warning")
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    
    response = RedirectResponse(url="/account", status_code=status.HTTP_302_FOUND)
    login_manager.set_cookie(response, get_user_access_cookie(user))
    return response


@router.post('/auth/otp/generate')
def Generate_OTP(request: Request, user: UserDB = Depends(login_manager)):
    
    if user.otp_enabled and user.otp_verified:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="OTP is already enabled for this user")
    
    otp_base32 = pyotp.random_base32()
    
    otp_auth_url = pyotp.totp.TOTP(otp_base32).provisioning_uri(
        name=user.username, issuer_name="dreamyskysanctuary.com")
    
    user.otp_base32 = otp_base32
    user.otp_auth_url = otp_auth_url
    user.otp_enabled = True
    user.otp_verified = False
    
    
    connection = create_connection("Website")
    update_otp_user(connection, user)
    close_connection(connection)

    return {'otp_enabled': True, "user": user.username, "otp_base32": otp_base32, "otp_auth_url": otp_auth_url}


@router.post('/auth/otp/verify')
def Verify_OTP(request: Request, payload: UserRequestSchema, user: UserDB = Depends(login_manager)):
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Token is invalid or user doesn't exist")
    
    if not user.otp_enabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="OTP is not enabled for this user")
    
    if user.otp_verified:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="OTP is already verified for this user")

    totp = pyotp.TOTP(user.otp_base32)
    print(f"{totp.now()} == {payload.token}")
    if not totp.verify(payload.token, valid_window=config.OTP_WINDOW):
        
        return {'otp_verified': False, "user": user.username}
        # raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
        #                     detail=message)
    
    user.otp_verified = True
    
    connection = create_connection("Website")
    update_otp_user(connection, user)
    close_connection(connection)

    return {'otp_verified': True, "user": user.username}


@router.post('/auth/otp/validate') # This is the endpoint that will be used to validate the OTP token, it will be used to authenticate the user after login
def Validate_OTP(request: Request, payload: UserRequestSchema, user: Annotated[UserDB, Security(login_manager)]):
    if not user.otp_enabled:
        return {'otp_valid': True, "user": user.username, "otp_enabled": False}

    if not user.otp_verified:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="OTP must be verified first, before using it to authenticate")

    totp = pyotp.TOTP(user.otp_base32)
    if not totp.verify(otp=payload.token, valid_window=config.OTP_WINDOW):
        return {'otp_valid': False, "user": user.username, "otp_enabled": True}

    return {'otp_valid': True, "user": user.username, "otp_enabled": True}


@router.post('/auth/otp/remove')
def Disable_OTP(request: Request, payload: UserRequestSchema, user: UserDB = Depends(login_manager)):
    if not user.otp_enabled:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="OTP must be enables first, before it can be disabled")
    
    if not user.otp_verified:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="OTP must be verified first, before it can be disabled. pls regenerate the OTP and verify it first")
    
    totp = pyotp.TOTP(user.otp_base32)
    if not totp.verify(otp=payload.token, valid_window=config.OTP_WINDOW):
        return {'otp_disabled': False, 'user': user.username}
    
    user.otp_enabled = False
    user.otp_verified = False
    user.otp_base32 = None
    user.otp_auth_url = None
    
    connection = create_connection("Website")
    update_otp_user(connection, user)
    close_connection(connection)

    return {'otp_disabled': True, 'user': user.username}


@router.get("/account")
def account(request: Request, user: Annotated[UserDB, Security(login_manager)]):
    return "You are an authentciated user"


@router.get("/admin")
def account(request: Request, user: Annotated[UserDB, Security(login_manager, scopes=[Scopes.ADMIN.value])]):
    return "You are an authentciated user"


@router.get("/logout")
def logout(request: Request, user: Annotated[UserDB, Security(login_manager)]):
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    print(login_manager.get_current_user(response))
    login_manager.set_cookie(response, "")
    return response


@router.get("/forgot-password")
def forgot_password(request: Request):
    return "You forgot your password"
