from typing import Dict, List

from fastapi import WebSocket


class ConnectionManager:

    def __init__(self):
        self.active_connections: Dict[
            str,
            List[WebSocket],
        ] = {}

    async def connect(
        self,
        websocket: WebSocket,
        interview_id: str,
    ):
        await websocket.accept()

        self.active_connections.setdefault(
            interview_id,
            [],
        ).append(websocket)

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

    def get_connections(
        self,
        interview_id: str,
    ) -> List[WebSocket]:
        return self.active_connections.get(
            interview_id,
            [],
        )

    async def send_personal_message(
        self,
        message: dict,
        websocket: WebSocket,
    ):
        try:
            await websocket.send_json(message)
        except Exception:
            pass

    async def broadcast(
        self,
        message: dict,
        interview_id: str,
    ):
        connections = self.get_connections(
            interview_id,
        ).copy()

        for connection in connections:
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