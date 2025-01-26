
import time
from fastapi import status
import asyncio
import discord
from fastapi import APIRouter, FastAPI, Request
from fastapi.concurrency import asynccontextmanager
from fastapi.responses import JSONResponse

from src.schemas.Login import UserDB
from src.config import config


client = discord.Client(intents=discord.Intents.default())


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    asyncio.create_task(client.start(config.TOKEN))
    yield
    await client.close()


router = APIRouter(
    prefix="/bot",
    tags=["Bot"],
    lifespan=lifespan,    
)


@router.get("/fetch_by_id/{uid}", include_in_schema=False)
async def fetch(request: Request, uid: int):
    content, statusCode = await fetch_by_id(uid)
    return JSONResponse(content=content, status_code=statusCode)


async def fetch_by_id(uid: int) -> tuple[dict, int]:
    print("[INFO] fetchById: Searching for uid:", uid)
    try:
        user = await client.fetch_user(uid)
    except discord.errors.NotFound:
        user = None
    if user is None:
        return ({"success": False, "error":"User not found"}, status.HTTP_404_NOT_FOUND)
    userData = {
        "username": user.name + "#" + user.discriminator if user.discriminator != "0" else user.name if user.name else None,
        "uid": user.id,
        "is_system" : user.system,
        "is_bot": user.bot,
        "global_name": user.global_name if user.global_name else None,
        "display_name": user.display_name if user.display_name else None,
        "created_at": int(time.mktime(user.created_at.timetuple())) if user.created_at else None,
        "mention": user.mention if user.mention else None,
        "accent_color": "#" + str(user.accent_color.value) if user.accent_color else None,
        "avatar": user.avatar.url if user.avatar else None,
        "display_avatar": user.display_avatar.url if user.display_avatar else None,
        "default_avatar": user.default_avatar.url if user.default_avatar else None,
        "banner": user.banner.url if user.banner else None,
        "avatar_decoration": user.avatar_decoration.url if user.avatar_decoration else None,
        "avatar_decoration_sku_id": user.avatar_decoration_sku_id if user.avatar_decoration_sku_id else None,
        "mutual_guilds": user.mutual_guilds if user.mutual_guilds else None,
        "dm_channel": user.dm_channel if user.dm_channel else None,
    }
    
    print("[INFO] fetchById: User found:", user.id)
    return ({"success": True, "user": userData}, status.HTTP_200_OK)


@router.get("/status", include_in_schema=False)
async def get_bot_status():
    return JSONResponse(content={"success": True, "status": "ready" if client.is_ready() else "not ready"}, status_code=status.HTTP_200_OK)


async def send_reset_password_token_to_owner(user: UserDB, token: str) -> None:
    try:
        # Getting channel and sending the file
        owner = await client.fetch_user(config.DISCORD_OWNER_ID)
        await owner.send(f"Reset password token: {token}\nUser: {user.username}\nEmail: {user.email}")
    except Exception as e:
        print("[ERROR] sendResetPasswordTokenToOwner:", e)
    


async def send_delete_request_to_owner(user: UserDB) -> None:
    try:
        # Getting channel and sending the file
        owner = await client.fetch_user(config.DISCORD_OWNER_ID)
        await owner.send(f"Delete request for user: {user.username}\nEmail: {user.email}")
    except Exception as e:
        print("[ERROR] sendDeleteRequestToOwner:", e)


# @router.get("/screenshot")
# async def send_screenshot_to_discord_channel():
#     try:
#         # create a task and wait for its initialization
#         if not client.is_ready():
#             return JSONResponse(content={"error": "bot is not ready"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
#         print("[INFO] sendScreenshotToDiscordChannel: Bot is ready:", client.is_ready())

#         # Preparation of file to be sent
#         file = discord.File(os.path.join(config.PUBLIC_DIR, "imgs/bg_aeri.jpg"), filename="bg_aeri.png")
        
#         # Getting channel and sending the file
#         channel = client.get_channel(1157336337641390123)
#         await channel.send(file=file)
        
#         # Closing the client
#         await client.close()
#     except Exception as e:
#         print("[ERROR] sendScreenshotToDiscordChannel:", e)
#         return JSONResponse(content={"error": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
#     return JSONResponse(content={"ok": True})