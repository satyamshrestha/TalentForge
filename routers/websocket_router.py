from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from pydantic import ValidationError

from db.database import SessionLocal
from schemas.websocket_schema import WebSocketAnswerMessage
from websocket.auth import authenticate_websocket
from websocket.authorization import can_access_interview
from websocket.events import WebSocketEvent
from websocket.manager import ConnectionManager


router = APIRouter(
    prefix="/ws",
    tags=["WebSocket"],
)

manager = ConnectionManager()


@router.websocket("/interview/{interview_id}")
async def interview_websocket(
    websocket: WebSocket,
    interview_id: str,
):
    user_id = await authenticate_websocket(websocket)

    if user_id is None:
        return

    db = SessionLocal()

    try:
        if not can_access_interview(
            db,
            user_id,
            interview_id,
        ):
            await websocket.close(code=1008)
            return
    finally:
        db.close()

    await manager.connect(
        websocket,
        interview_id,
    )

    try:
        await manager.broadcast_event(
            WebSocketEvent.INTERVIEW_STARTED,
            {
                "interview_id": interview_id,
                "user_id": user_id,
            },
            interview_id,
        )

        while True:
            data = await websocket.receive_text()

            try:
                message = WebSocketAnswerMessage.model_validate_json(
                    data
                )

            except ValidationError:
                await websocket.send_json(
                    {
                        "event": "error",
                        "message": "Invalid answer message.",
                    }
                )
                continue

            answer_text = message.answer.strip()

            await manager.broadcast_event(
                WebSocketEvent.ANSWER_SUBMITTED,
                {
                    "interview_id": interview_id,
                    "user_id": user_id,
                    "message": answer_text,
                },
                interview_id,
            )

    except WebSocketDisconnect:
        manager.disconnect(
            websocket,
            interview_id,
        )

    except Exception:
        manager.disconnect(
            websocket,
            interview_id,
        )

        await websocket.close(code=1011)