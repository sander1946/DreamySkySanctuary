from typing import Annotated

from fastapi import APIRouter, Depends, Form, Request, Security, status
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi_login import LoginManager

from pydantic import EmailStr
import pyotp
from werkzeug.security import generate_password_hash, check_password_hash

from src.routes.bot.bot import send_reset_password_token_to_owner
from src.utils.flash import get_flashed_messages, flash, FlashCategory
from src.config import config
from src.schemas.Login import ForgotPasswordForm, LoginForm, RegisterForm, ResetPasswordForm, Scopes, UserDB, UserRequestSchema
from src.utils.database import close_connection, create_connection, create_user, get_forgot_password_account_from_token, get_user_by_email, get_user_by_username, remove_forgot_password_token, save_forgot_password_token, update_otp_user, update_user_details, update_user_name

login_manager = LoginManager(config.SERVER_SECRET, token_url="/auth/login", use_cookie=True)
login_manager.cookie_name = "user_token"

templates = Jinja2Templates(directory=config.TEMPLATES_DIR)
templates.env.globals["get_flashed_messages"] = get_flashed_messages
templates.env.globals["FlashCategory"] = FlashCategory

router = APIRouter(
    prefix="",
    tags=["Authentication"],
)


def get_user_access_cookie(user: UserDB):
    scopes = [Scopes.BASIC.value if not user.is_admin else Scopes.ADMIN.value]
    if not user.otp_enabled:
        scopes.append(Scopes.OTP_CHECKED.value)
    
    access_token = login_manager.create_access_token(
        data={
            "sub": user.username
            },
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
def register(request: Request, register_data: Annotated[RegisterForm, Form(media_type="application/x-www-form-urlencoded")]):
    username = register_data.username
    email = register_data.email
    password = register_data.password
    password_hash = generate_password_hash(password)
    
    connection = create_connection("Website")
    user = get_user_by_username(connection, username)
    
    if user:
        print(f"User already exists: {user.username}")
        return JSONResponse(
            content={
                "success": False, 
                "detail": "A user by that username already exists. Chose a diffrent username or try to login", 
                "category": FlashCategory.INFO.value, 
                "user": user.username
                },
            status_code=status.HTTP_202_ACCEPTED
        )
    
    userDB = UserDB(username=username, email=email, password_hash=password_hash)
    
    create_user(connection, userDB)
    close_connection(connection)
    
    print(f"User created: {userDB.username}")
    
    response = JSONResponse(
        content={
            "success": True, 
            "user": username,
            "redirect": "/account"
            }, 
        status_code=status.HTTP_201_CREATED
        )
    login_manager.set_cookie(response, get_user_access_cookie(userDB))
    return response



@router.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})


@router.post("/auth/login")
def login(request: Request, login_data: Annotated[LoginForm, Form(media_type="application/x-www-form-urlencoded")]):
    username = login_data.username
    password = login_data.password
    
    user: UserDB = load_user(username)
    
    if not user:
        return JSONResponse(
            content={
                "success": False, 
                "detail": "The username or password is incorrect", 
                "category": FlashCategory.WARNING.value, 
                "user": username
                },
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    
    if not check_user_password(user, password):
        return JSONResponse(
            content={
                "success": False, 
                "detail": "The username or password is incorrect", 
                "category": FlashCategory.WARNING.value, 
                "user": username
                },
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    
    response = JSONResponse(
        content={
            "success": True, 
            "user": user.username,
            "redirect": "/account"
            }, 
        status_code=status.HTTP_200_OK
        )
    
    login_manager.set_cookie(response, get_user_access_cookie(user))
    return response


@router.post('/auth/otp/generate')
def Generate_OTP(request: Request, user: UserDB = Depends(login_manager)):
    
    if user.otp_enabled and user.otp_verified:
        return JSONResponse(
            content={
                "success": False, 
                "detail": "OTP is already enabled for this user", 
                "category": FlashCategory.WARNING.value, 
                "user": user.username
                },
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    otp_base32 = pyotp.random_base32()
    
    otp_auth_url = pyotp.totp.TOTP(otp_base32).provisioning_uri(
        name=user.username, issuer_name="DreamySkySanctuary.com")
    
    user.otp_base32 = otp_base32
    user.otp_auth_url = otp_auth_url
    user.otp_enabled = True
    user.otp_verified = False
    
    
    connection = create_connection("Website")
    update_otp_user(connection, user)
    close_connection(connection)

    return JSONResponse(
        content={
            "success": True, 
            "user": user.username, 
            "otp_base32": otp_base32, 
            "otp_auth_url": otp_auth_url
            },
        status_code=status.HTTP_200_OK
    )


@router.post('/auth/otp/verify')
def Verify_OTP(request: Request, payload: UserRequestSchema, user: UserDB = Depends(login_manager)):
    if not user:
        return JSONResponse(
            content={
                "success": False, 
                "detail": "Token is invalid or user doesn't exist",
                "category": FlashCategory.WARNING.value, 
                "user": user.username
                },
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    if not user.otp_enabled:
        return JSONResponse(
            content={
                "success": False, 
                "detail": "OTP is not enabled for this user", 
                "category": FlashCategory.WARNING.value, 
                "user": user.username
                },
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    if user.otp_verified:
        return JSONResponse(
            content={
                "success": False, 
                "detail": "OTP is already verified for this user", 
                "category": FlashCategory.WARNING.value, 
                "user": user.username
                },
            status_code=status.HTTP_400_BAD_REQUEST
        )

    totp = pyotp.TOTP(user.otp_base32)
    print(f"{totp.now()} == {payload.token}")
    if not totp.verify(payload.token, valid_window=config.OTP_WINDOW):
        return JSONResponse(
            content={
                "success": False, 
                "detail": "Invalid OTP token", 
                "category": FlashCategory.WARNING.value, 
                "user": user.username
                },
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    user.otp_verified = True
    
    connection = create_connection("Website")
    update_otp_user(connection, user)
    close_connection(connection)

    return JSONResponse(
        content={
            "success": True, 
            "user": user.username
            },
        status_code=status.HTTP_200_OK
    )


@router.post('/auth/otp/validate') # This is the endpoint that will be used to validate the OTP token, it will be used to authenticate the user after login
def Validate_OTP(request: Request, payload: UserRequestSchema, user: Annotated[UserDB, Security(login_manager)]):
    if not user.otp_enabled:
        return JSONResponse(
            content={
                "success": False, 
                "detail": "OTP is not enabled for this user", 
                "category": FlashCategory.WARNING.value, 
                "user": user.username
                },
            status_code=status.HTTP_400_BAD_REQUEST
        )

    if not user.otp_verified:
        return JSONResponse(
            content={
                "success": False, 
                "detail": "OTP must be verified first, before using it to authenticate", 
                "category": FlashCategory.WARNING.value, 
                "user": user.username
                },
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    totp = pyotp.TOTP(user.otp_base32)
    if not totp.verify(otp=payload.token, valid_window=config.OTP_WINDOW):
        return JSONResponse(
            content={
                "success": False, 
                "detail": "Invalid OTP token", 
                "category": FlashCategory.WARNING.value, 
                "user": user.username
                },
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    return JSONResponse(
        content={
            "success": True, 
            "user": user.username,
            "redirect": "/account"
            },
        status_code=status.HTTP_200_OK
    )


@router.post('/auth/otp/remove')
def Disable_OTP(request: Request, payload: UserRequestSchema, user: UserDB = Depends(login_manager)):
    if not user.otp_enabled:
        return JSONResponse(
            content={
                "success": False, 
                "detail": "OTP is not enabled for this user", 
                "category": FlashCategory.WARNING.value, 
                "user": user.username
                },
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    if not user.otp_verified:
        return JSONResponse(
            content={
                "success": False, 
                "detail": "OTP must be verified first, before it can be disabled. pls regenerate the OTP and verify it first", 
                "category": FlashCategory.WARNING.value, 
                "user": user.username
                },
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    totp = pyotp.TOTP(user.otp_base32)
    if not totp.verify(otp=payload.token, valid_window=config.OTP_WINDOW):
        return JSONResponse(
            content={
                "success": False, 
                "detail": "Invalid OTP token", 
                "category": FlashCategory.WARNING.value, 
                "user": user.username
                },
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    
    user.otp_enabled = False
    user.otp_verified = False
    user.otp_base32 = None
    user.otp_auth_url = None
    
    connection = create_connection("Website")
    update_otp_user(connection, user)
    close_connection(connection)

    return JSONResponse(
        content={
            "success": True, 
            'user': user.username
            },
        status_code=status.HTTP_200_OK
    )


@router.get("/account")
def account(request: Request, user: Annotated[UserDB, Security(login_manager)]):
    return templates.TemplateResponse("auth/account.html", {"request": request, "user": user})


@router.get("/admin")
def account(request: Request, user: Annotated[UserDB, Security(login_manager, scopes=[Scopes.ADMIN.value])]):
    return "You are an authentciated admin"


@router.get("/logout")
def logout_page(request: Request):
    print("Logging out")    
    response = RedirectResponse(
        url="/login",
        status_code=status.HTTP_307_TEMPORARY_REDIRECT
    )
    login_manager.set_cookie(response, "")
    return response


@router.post("/auth/logout")
def logout(request: Request, user: Annotated[UserDB, Security(login_manager)]):
    response = JSONResponse(
        content={
            "success": True, 
            "user": user.username,
            "redirect": "/login"
            }, 
        status_code=status.HTTP_200_OK
    )
    login_manager.set_cookie(response, "")
    return response


@router.get("/forgot-password")
def forgot_password(request: Request):
    return templates.TemplateResponse("auth/forgot-password.html", {"request": request})


@router.post("/auth/forgot-password")
async def forgot_password(request: Request, forgotForm: Annotated[ForgotPasswordForm, Form(media_type="application/x-www-form-urlencoded")]):
    
    if not forgotForm.account:
        flash(request, "Please provide an account to reset password", FlashCategory.WARNING.value)
        return JSONResponse(
            content={
                "success": False, 
                "detail": "Please provide an account to reset password",
                "category": FlashCategory.WARNING.value
                },
            status_code=status.HTTP_302_FOUND
        )
    
    connection = create_connection("Website")
    if forgotForm.account.find("@") != -1:
        user: UserDB = get_user_by_email(connection, forgotForm.account)
    else:
        user: UserDB = get_user_by_username(connection, forgotForm.account)

    if not user:
        close_connection(connection)
        return JSONResponse(
            content={
                "success": True, 
                "detail": "A password reset link has been sent to your email if it's associated with an account",
                "category": FlashCategory.SUCCESS.value, 
                "user": forgotForm.account
                },
            status_code=status.HTTP_200_OK
        )
    
    reset_token = pyotp.random_base32(length=64)
    
    save_forgot_password_token(connection, user, reset_token)
    
    close_connection(connection)
    
    # TODO: send email with reset token
    await send_reset_password_token_to_owner(user, reset_token)
    return JSONResponse(
            content={
                "success": True, 
                "detail": "A password reset link has been sent to your email if it's associated with an account",
                "category": FlashCategory.SUCCESS.value, 
                "user": user.username
                },
            status_code=status.HTTP_200_OK
        )


@router.get("/reset-password/{token}")
def reset_password_page(request: Request, token: str):
    connection = create_connection("Website")
    user = get_forgot_password_account_from_token(connection, token)
    close_connection(connection)
    
    if not user:
        return RedirectResponse(url="/forgot-password", status_code=status.HTTP_302_FOUND)

    return templates.TemplateResponse("auth/reset-password.html", {"request": request, "token": token})


@router.post("/auth/reset-password/{token}")
def reset_password(request: Request, token: str, resetPasswordFrom: Annotated[ResetPasswordForm, Form(media_type="application/x-www-form-urlencoded")]):
    
    connection = create_connection("Website")
    user = get_forgot_password_account_from_token(connection, token)
    
    if not user:
        close_connection(connection)
        return JSONResponse(
            content={
                "success": False, 
                "detail": "Invalid reset token",
                "category": FlashCategory.WARNING.value
                },
            status_code=status.HTTP_302_FOUND
        )
    
    user.password_hash = generate_password_hash(resetPasswordFrom.password)
    
    update_user_details(connection, user)
    
    remove_forgot_password_token(connection, token)
    
    close_connection(connection)
    
    flash(request, "Password has been reset successfully", FlashCategory.SUCCESS.value)
    
    return JSONResponse(
        content={
            "success": True, 
            "detail": "Password has been reset successfully",
            "category": FlashCategory.SUCCESS.value, 
            "user": user.username,
            "redirect": "/login"
            },
        status_code=status.HTTP_200_OK
    )


@router.post("/auth/change-username")
def change_username(request: Request, user: Annotated[UserDB, Security(login_manager)], username: Annotated[str, Form(media_type="application/x-www-form-urlencoded")]):
    connection = create_connection("Website")
    current_user = get_user_by_username(connection, username)
    
    if current_user:
        print(f"User already exists: {user.username}")
        return JSONResponse(
            content={
                "success": False, 
                "detail": "A user by that username already exists. Chose a diffrent username or try to login", 
                "category": FlashCategory.INFO.value, 
                "user": user.username
                },
            status_code=status.HTTP_202_ACCEPTED
        )
    
    update_user_name(connection, user, username)
    
    response = JSONResponse(
        content={
            "success": True, 
            "detail": "Username has been changed successfully",
            "user": user.username,
            "redirect": "/login"
            },
        status_code=status.HTTP_200_OK
        )
    login_manager.set_cookie(response, get_user_access_cookie(user))
    return response

@router.post("/auth/change-email")
def change_email(request: Request, user: Annotated[UserDB, Security(login_manager)], email: Annotated[EmailStr, Form(media_type="application/x-www-form-urlencoded")]):
    connection = create_connection("Website")
    
    user.email = email
    
    update_user_details(connection, user)  
    
    close_connection(connection)
    
    return JSONResponse(
        content={
            "success": True, 
            "detail": "Email has been changed successfully",
            "user": user.username,
            "redirect": "/account"
            },
        status_code=status.HTTP_200_OK
    )

@router.post("/auth/change-password")
def change_password(request: Request, user: Annotated[UserDB, Security(login_manager)], resetPasswordFrom: Annotated[ResetPasswordForm, Form(media_type="application/x-www-form-urlencoded")]):
    connection = create_connection("Website")
    
    user.password_hash = generate_password_hash(resetPasswordFrom.password)
    
    update_user_details(connection, user)  
    
    close_connection(connection)
    
    print(f"Password changed for: {user.username}")
    
    return JSONResponse(
        content={
            "success": True, 
            "detail": "Password has been changed successfully",
            "user": user.username,
            "redirect": "/account"
            },
        status_code=status.HTTP_200_OK
    )
