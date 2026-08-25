from collections import defaultdict

from fastapi import WebSocket


class ConnectionManager:

    def __init__(self):
        self.active_connections: dict[str, list[WebSocket]] = defaultdict(list)

    async def connect(
        self,
        websocket: WebSocket,
        interview_id: str,
    ):
        await websocket.accept()

        self.active_connections[interview_id].append(
            websocket
        )

    def disconnect(
        self,
        websocket: WebSocket,
        interview_id: str,
    ):
        connections = self.active_connections.get(interview_id)

        if not connections:
            return

        if websocket in connections:
            connections.remove(websocket)

        if not connections:
            del self.active_connections[interview_id]

    async def send_personal_message(
        self,
        message: dict,
        websocket: WebSocket,
    ):
        await websocket.send_json(message)

    async def broadcast_event(
        self,
        event: str,
        data: dict,
        interview_id: str,
    ):
        message = {
            "event": event,
            "data": data,
        }

        connections = self.active_connections.get(
            interview_id,
            [],
        )

        for connection in connections.copy():
            try:
                await connection.send_json(message)
            except Exception:
                self.disconnect(
                    connection,
                    interview_id,
                )