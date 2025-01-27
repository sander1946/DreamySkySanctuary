import os
from src.logger import Logger
from src.utils.database import get_image_from_db
import datetime	as datetime

logger = Logger()

async def remove_expired_files(connection, path) -> None:
    filenames = next(os.walk(path), (None, None, []))[2]  # [] if no file
    for filename in filenames:
        file_path = os.path.join(path, filename)
        image_data = get_image_from_db(connection, filename)
        if image_data is None:
            logger.log("PRINT", f"File {filename} removed due to it not being in the database.")
            os.remove(file_path)
            continue
        if image_data.delete_after is None:
            continue
        if os.path.exists(file_path) is False:
            logger.log("PRINT", f"File {filename} removed due to it not existing.")
            continue
        if os.path.getmtime(file_path) > image_data.delete_after.timestamp(): # if the file is older than the expiration time
            logger.log("PRINT", f"File {filename} removed due to expiration.")
            os.remove(file_path)