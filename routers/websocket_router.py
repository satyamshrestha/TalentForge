from fastapi import APIRouter, WebSocket, WebSocketDisconnect

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
        while True:
            data = await websocket.receive_text()

            await manager.send_personal_message(
                data,
                websocket,
            )

    except WebSocketDisconnect:
        manager.disconnect(
            websocket,
            interview_id,
        )