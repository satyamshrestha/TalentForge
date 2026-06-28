from fastapi import Depends, HTTPException, status
from auth.deps import get_current_user
from auth.jwt_handler import verify_access_token
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def require_scope(scope: str):
    def scope_checker(
        token: str = Depends(oauth2_scheme),
        current_user=Depends(get_current_user)
    ):
        payload = verify_access_token(token)

        if payload is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token."
            )

        scopes = payload.get("scopes", [])

        if scope not in scopes:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient scope."
            )

        return current_user

    return scope_checker