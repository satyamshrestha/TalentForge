import json

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from db.database import SessionLocal
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
                message = json.loads(data)
            except json.JSONDecodeError:
                await websocket.send_json(
                    {
                        "event": "error",
                        "message": "Invalid JSON message.",
                    }
                )
                continue

            if not isinstance(message, dict):
                await websocket.send_json(
                    {
                        "event": "error",
                        "message": "Message must be a JSON object.",
                    }
                )
                continue

            answer_text = message.get("answer")

            if not isinstance(answer_text, str):
                await websocket.send_json(
                    {
                        "event": "error",
                        "message": "Answer must be a string.",
                    }
                )
                continue

            answer_text = answer_text.strip()

            if not answer_text:
                await websocket.send_json(
                    {
                        "event": "error",
                        "message": "Answer cannot be empty.",
                    }
                )
                continue

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