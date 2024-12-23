class FileTypeException(Exception):
    def __init__(self, file_name: str, file_type: str, allowed_types: list, message: str | None = None):
        self.file_name: str = file_name
        self.file_type: str = file_type
        self.allowed_types: list = allowed_types
        if message != None:
            self.message: str = message
        else:
            self.message: str = f"File of type '{file_type}' is not allowed here."