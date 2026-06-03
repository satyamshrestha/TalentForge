from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

from utils.config import settings

def create_access_token(data: dict):
    payload = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    payload.update({
        "exp": expire
    })
    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

def verify_access_token(token: str):
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=settings.ALGORITHM
        )
        
        return payload
    
    except JWTError:
        return None
    