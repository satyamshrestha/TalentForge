from fastapi import APIRouter, WebSocket, WebSocketDisconnect

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
    await manager.connect(
        websocket,
        interview_id,
    )

    try:
        await manager.broadcast_event(
            WebSocketEvent.INTERVIEW_STARTED,
            {
                "interview_id": interview_id,
            },
            interview_id,
        )

        while True:
            data = await websocket.receive_text()

            await manager.broadcast_event(
                WebSocketEvent.ANSWER_SUBMITTED,
                {
                    "interview_id": interview_id,
                    "message": data,
                },
                interview_id,
            )

    except WebSocketDisconnect:
        manager.disconnect(
            websocket,
            interview_id,
        )