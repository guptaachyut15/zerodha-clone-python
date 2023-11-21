from fastapi.security import HTTPBearer
from fastapi.exceptions import HTTPException
from fastapi import Depends
from src.utils.jwt import de_construct_jwt
from src.utils.logger import LOG

security = HTTPBearer()


def has_access(credentials=Depends(security)):
    try:
        if not credentials or not credentials.credentials:
            raise HTTPException(
                400, {"status": "failed", "error": "JWT Token not found"}
            )
        payload = de_construct_jwt(credentials.credentials)
        return payload
    except Exception as e:
        raise HTTPException(400, {"status": "failed", "error": "Dont have the access"})
