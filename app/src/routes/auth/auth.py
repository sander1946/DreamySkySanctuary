import io
from typing import Annotated

from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse, StreamingResponse
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException

import pyotp
from werkzeug.security import generate_password_hash, check_password_hash

from src.schemas.errors.NotAuthenticatedException import NotAuthenticatedException
from src.config import config
from src.schemas.Login import LoginForm, RegisterForm, User, UserDB, UserRequestSchema
from src.utils.database import close_connection, create_connection, create_user, get_user_by_username, update_otp_user

import qrcode

login_manager = LoginManager(config.SERVER_SECRET, token_url="/auth/login", use_cookie=True, not_authenticated_exception=NotAuthenticatedException)
login_manager.cookie_name = "user_token"


router = APIRouter(
    prefix="/auth",
    tags=["Upload"],
)


@login_manager.user_loader()
def load_user(username: str) -> UserDB:
    connection = create_connection("Website")
    user = get_user_by_username(connection, username)
    close_connection(connection)
    return user


def check_user_password(user: UserDB, plain_password: str) -> bool:
    return check_password_hash(user.password_hash, plain_password)


@router.get("/register")
def register_page():
    return HTMLResponse("""
    <form method="post">
    <input type="text" name="username" autocomplete="off" required>
    <input type="email" name="email" required>
    <input type="text" name="discord" required>
    <input type="password" name="password" required>
    <button type="submit">Register</button>
    </form>
    """)


@router.post("/register")
def register(register_data: Annotated[RegisterForm, Form()]):
    username = register_data.username
    email = register_data.email
    discord = register_data.discord
    password = register_data.password
    password_hash = generate_password_hash(password)
    
    connection = create_connection("Website")
    user = get_user_by_username(connection, username)
    
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
    
    userDB = UserDB(username=username, email=email, discord=discord, password_hash=password_hash)
    
    create_user(connection, userDB)
    close_connection(connection)
    return RedirectResponse(url="/auth/login", status_code=status.HTTP_302_FOUND)


@router.get("/login")
def login_page():
    return HTMLResponse("""
    <form method="post">
    <input type="text" name="username" autocomplete="off" required>
    <input type="password" name="password" required>
    <button type="submit">Login</button>
    </form>
    """)


@router.post("/login")
def login(login_data: Annotated[LoginForm, Form()]):
    username = login_data.username
    password = login_data.password
    
    user: UserDB = load_user(username)
    
    if not user:
        raise InvalidCredentialsException
    
    if not check_user_password(user, password):
        print("Password is incorrect")
        raise NotAuthenticatedException()
    
    access_token = login_manager.create_access_token(
        data={"sub": username},
        expires=config.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    response = RedirectResponse(url="/auth/account", status_code=status.HTTP_302_FOUND)
    login_manager.set_cookie(response, access_token)
    return response


@router.post('/otp/generate')
def Generate_OTP(payload: UserRequestSchema, user: UserDB = Depends(login_manager)):
    otp_base32 = pyotp.random_base32()
    
    otp_auth_url = pyotp.totp.TOTP(otp_base32).provisioning_uri(
        name=user.username, issuer_name="dreamyskysanctuary.com")

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No user with this username: {payload.username} found')
    
    user.otp_base32 = otp_base32
    user.otp_auth_url = otp_auth_url
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(otp_auth_url)
    qr.make(fit=True)
    

    img = qr.make_image(fill_color="black", back_color="white")
    img.save("/dreamy-data/otp.png")
    
    connection = create_connection("Website")
    update_otp_user(connection, user)
    close_connection(connection)

    return FileResponse("/dreamy-data/otp.png")
    return {'base32': otp_base32, "otpauth_url": otp_auth_url}



@router.post('/otp/verify')
def Verify_OTP(payload: UserRequestSchema, user: UserDB = Depends(login_manager)):
    message = "Token is invalid or user doesn't exist"

    totp = pyotp.TOTP(user.otp_base32)
    print(f"{totp.now()} == {payload.token}")
    if not totp.verify(payload.token, valid_window=2):
        
        return {'otp_verified': False, "user": user.username}
        # raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
        #                     detail=message)
    
    user.otp_verified = True
    user.otp_enabled = True
    
    connection = create_connection("Website")
    update_otp_user(connection, user)
    close_connection(connection)

    return {'otp_verified': True, "user": user.username}


@router.post('/otp/validate')
def Validate_OTP(payload: UserRequestSchema):
    message = "Token is invalid or user doesn't exist"
    
    user = load_user(payload.username)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=message)

    if not user.otp_verified:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="OTP must be verified first")

    totp = pyotp.TOTP(user.otp_base32)
    if not totp.verify(otp=payload.token, valid_window=1):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=message)

    return {'otp_valid': True}


@router.post('/otp/remove')
def Disable_OTP(payload: UserRequestSchema, user: UserDB = Depends(login_manager)):
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No user with this username: {payload.username} found')
    
    user.otp_enabled = False
    user.otp_verified = False
    user.otp_base32 = None
    user.otp_auth_url = None
    
    connection = create_connection("Website")
    update_otp_user(connection, user)
    close_connection(connection)

    return {'otp_disabled': True, 'user': user.username}


@router.get("/account")
def account(user: UserDB = Depends(login_manager)):
    return "You are an authentciated user"


@router.get("/logout")
def logout():
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    print(login_manager.get_current_user(response))
    login_manager.set_cookie(response, "")
    return response
