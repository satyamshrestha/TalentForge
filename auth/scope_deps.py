from fastapi import Depends, HTTPException, status
from auth.deps import get_current_user, get_token_payload


def require_scope(scope: str):
    def scope_checker(
        payload=Depends(get_token_payload),
        current_user=Depends(get_current_user)
    ):
        scopes = payload.get("scopes", [])

        if scope not in scopes:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient scope."
            )

        return current_user

    return scope_checker