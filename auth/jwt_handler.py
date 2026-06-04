from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

from utils.config import settings

def create_access_token(data: dict):
    payload = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    payload.update({
        "exp": expire,
        "type": "access"  
    })
    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

def create_refresh_token(data: dict):
    payload = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=7)
    payload.update({
        "exp": expire,
        "type": "refresh"
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
        if payload.get("type") != "access":
            return None 
        
        return payload
    
    except JWTError:
        return None
    
def verify_refresh_token(token: str):
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=settings.ALGORITHM
        )
        if payload.get("type") != "refresh":
            return None

        return payload
    
    except JWTError:
        return None
    