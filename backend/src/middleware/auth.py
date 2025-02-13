from fastapi import HTTPException, Request
from itsdangerous import URLSafeSerializer
from config.settings import config


serializer = URLSafeSerializer(config.SECRET_KEY)


def get_current_user(request: Request):
    """Retrieves the current user from the session cookie."""
    session_token = request.cookies.get("session_id")
    if not session_token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        session_data = serializer.loads(session_token)
        return session_data["user_id"]
    except:
        raise HTTPException(status_code=401, detail="Invalid session")
