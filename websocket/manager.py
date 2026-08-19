from collections import defaultdict

from fastapi import WebSocket


class ConnectionManager:

    def __init__(self):
        self.active_connections: dict[
            str,
            list[WebSocket],
        ] = defaultdict(list)

    async def connect(
        self,
        websocket: WebSocket,
        interview_id: str,
    ):
        await websocket.accept()

        self.active_connections[
            interview_id
        ].append(websocket)

    def disconnect(
        self,
        websocket: WebSocket,
        interview_id: str,
    ):
        connections = self.active_connections.get(
            interview_id,
            [],
        )

        if websocket in connections:
            connections.remove(websocket)

        if not connections:
            self.active_connections.pop(
                interview_id,
                None,
            )

    async def send_personal_message(
        self,
        message: str,
        websocket: WebSocket,
    ):
        await websocket.send_text(message)

    async def broadcast(
        self,
        message: str,
        interview_id: str,
    ):
        connections = self.active_connections.get(
            interview_id,
            [],
        )

        for connection in connections:
            await connection.send_text(message)

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

        for connection in connections:
            await connection.send_json(message)