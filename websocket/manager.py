from typing import Dict, Set

from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, Set[WebSocket]] = {}

    async def connect(
        self,
        websocket: WebSocket,
        interview_id: str,
    ):
        await websocket.accept()

        connections = self.active_connections.setdefault(
            interview_id,
            set(),
        )

        connections.add(websocket)

    def disconnect(
        self,
        websocket: WebSocket,
        interview_id: str,
    ):
        connections = self.active_connections.get(interview_id)

        if not connections:
            return

        connections.discard(websocket)

        if not connections:
            self.active_connections.pop(
                interview_id,
                None,
            )

    async def send_personal_message(
        self,
        message: dict,
        websocket: WebSocket,
    ):
        await websocket.send_json(message)

    async def broadcast_event(
        self,
        event,
        data: dict,
        interview_id: str,
    ):
        message = {
            "event": event,
            "data": data,
        }

        connections = self.active_connections.get(
            interview_id,
            set(),
        )

        disconnected = set()

        for connection in connections.copy():
            try:
                await connection.send_json(message)
            except Exception:
                disconnected.add(connection)

        for connection in disconnected:
            self.disconnect(
                connection,
                interview_id,
            )

    def get_connection_count(
        self,
        interview_id: str,
    ) -> int:
        return len(
            self.active_connections.get(
                interview_id,
                set(),
            )
        )