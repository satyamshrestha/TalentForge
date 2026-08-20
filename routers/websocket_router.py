from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from websocket.auth import authenticate_websocket
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

            await manager.broadcast_event(
                WebSocketEvent.ANSWER_SUBMITTED,
                {
                    "interview_id": interview_id,
                    "user_id": user_id,
                    "message": data,
                },
                interview_id,
            )

    except WebSocketDisconnect:
        manager.disconnect(
            websocket,
            interview_id,
        )