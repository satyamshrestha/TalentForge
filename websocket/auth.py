from fastapi import WebSocket
from jose import JWTError, jwt

from utils.config import settings


async def authenticate_websocket(
    websocket: WebSocket,
):
    token = websocket.query_params.get("token")

    if not token:
        await websocket.close(
            code=1008,
            reason="Authentication required.",
        )
        return None

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        user_id = payload.get("sub")

        if not user_id:
            await websocket.close(
                code=1008,
                reason="Invalid authentication token.",
            )
            return None

        return user_id

    except JWTError:
        await websocket.close(
            code=1008,
            reason="Invalid authentication token.",
        )
        return None