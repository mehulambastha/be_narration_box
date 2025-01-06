from fastapi import Security, HTTPException
from fastapi.security.api_key import APIKeyHeader
import os
from dotenv import load_dotenv
from ..logging import logger

load_dotenv()

API_KEY = os.getenv("SSE_API_KEY")  # Store in environment variables
api_key_header = APIKeyHeader(name="X-API-Key")


async def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        logger.error(f"Wrong API Key in stream.. Provided {api_key}")
        raise HTTPException(status_code=403)
    return api_key
