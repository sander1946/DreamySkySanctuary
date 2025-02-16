class FileNotFoundException(Exception):
    def __init__(self, file_name: str, file_path: str | None = None, message: str | None = None):
        self.file_name: str = file_name
        if file_path == None:
            self.file_path: str = file_path
            if message != None:
                self.message: str = message
            else:
                self.message: str = f"The file '{file_name}' was not found'."
        else:
            if message != None:
                self.message: str = message
            else:
                self.message: str = f"The file '{file_name}' was not found in '{file_path}'."