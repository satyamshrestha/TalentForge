from typing import Dict, List

from fastapi import WebSocket


class ConnectionManager:

    def __init__(self):
        self.active_connections: Dict[
            str,
            List[WebSocket]
        ] = {}

    async def connect(
        self,
        websocket: WebSocket,
        interview_id: str,
    ):
        await websocket.accept()

        if interview_id not in self.active_connections:
            self.active_connections[interview_id] = []

        self.active_connections[interview_id].append(
            websocket
        )

    def disconnect(
        self,
        websocket: WebSocket,
        interview_id: str,
    ):
        connections = self.active_connections.get(
            interview_id,
            []
        )

        if websocket in connections:
            connections.remove(websocket)

        if not connections:
            self.active_connections.pop(
                interview_id,
                None
            )

    def get_connections(
        self,
        interview_id: str,
    ) -> List[WebSocket]:
        return self.active_connections.get(
            interview_id,
            []
        )

    async def send_personal_message(
        self,
        message: dict,
        websocket: WebSocket,
    ):
        await websocket.send_json(message)

    async def broadcast(
        self,
        message: dict,
        interview_id: str,
    ):
        connections = self.get_connections(interview_id)

        for connection in connections.copy():
            try:
                await connection.send_json(message)
            except Exception:
                self.disconnect(
                    connection,
                    interview_id,
                )

    async def broadcast_event(
        self,
        event: str,
        data: dict,
        interview_id: str,
    ):
        await self.broadcast(
            {
                "event": event,
                "data": data,
            },
            interview_id,
        )