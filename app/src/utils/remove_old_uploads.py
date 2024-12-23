import os
import time


def remove_expired_files(path, expire_time) -> None:
    filenames = next(os.walk(path), (None, None, []))[2]  # [] if no file
    for file in filenames:
        file_path = os.path.join(path, file)
        if os.path.getmtime(file_path) < time.time() - expire_time: 
            os.remove(file_path)
            print(f"File {file} removed due to expiration.")