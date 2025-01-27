
import time
from fastapi import status
import discord
from discord.ext import commands

from src.schemas.Login import UserDB
from src.logger import Logger

logger = Logger()

client = discord.Client(intents=discord.Intents.default())

async def fetch_by_id(uid: int) -> tuple[dict, int]:
    logger.log("INFO", f"Fetching user with id: {uid}")
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
    
    logger.log("INFO", f"User with id: {uid} fetched.")
    return ({"success": True, "user": userData}, status.HTTP_200_OK)
