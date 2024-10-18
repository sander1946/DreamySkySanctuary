from fastapi import FastAPI, HTTPException, Security, status
from fastapi.security import APIKeyHeader

api_keys: list[str] = [
    "0123456789abcdef0123456789abcdef",
]

api_key_header = APIKeyHeader(name="Key")

def get_api_key(api_key_header: str = Security(api_key_header)) -> str:
    if api_key_header in api_keys:
        return api_key_header
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key",
    )