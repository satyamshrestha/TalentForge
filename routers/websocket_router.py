import logging

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from pydantic import ValidationError

from db.database import SessionLocal
from schemas.websocket_schema import WebSocketAnswerMessage
from services.deps import get_answer_service
from websocket.auth import authenticate_websocket
from websocket.authorization import (
    can_access_interview,
    can_access_question,
)
from websocket.events import WebSocketEvent
from websocket.manager import ConnectionManager


logger = logging.getLogger("talentforge.websocket")


router = APIRouter(
    prefix="/ws",
    tags=["WebSocket"],
)

manager = ConnectionManager()


@router.websocket("/interview/{interview_id}")
async def interview_websocket(
    websocket: WebSocket,
    interview_id: str,
    answer_service=Depends(get_answer_service),
):
    user_id = await authenticate_websocket(
        websocket,
    )

    if user_id is None:
        return

    db = SessionLocal()

    try:
        if not can_access_interview(
            db,
            user_id,
            interview_id,
        ):
            await websocket.close(
                code=1008,
                reason="Access denied.",
            )
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
                message = (
                    WebSocketAnswerMessage
                    .model_validate_json(data)
                )

            except ValidationError:
                await manager.send_personal_message(
                    {
                        "event": WebSocketEvent.ERROR,
                        "data": {
                            "message": (
                                "Invalid answer message."
                            ),
                        },
                    },
                    websocket,
                )
                continue

            answer_text = message.answer.strip()

            if not answer_text:
                await manager.send_personal_message(
                    {
                        "event": WebSocketEvent.ERROR,
                        "data": {
                            "message": (
                                "Answer cannot be empty."
                            ),
                        },
                    },
                    websocket,
                )
                continue

            db = SessionLocal()

            try:
                if not can_access_question(
                    db,
                    user_id,
                    interview_id,
                    message.question_id,
                ):
                    await manager.send_personal_message(
                        {
                            "event": WebSocketEvent.ERROR,
                            "data": {
                                "message": (
                                    "Question does not belong "
                                    "to this interview."
                                ),
                            },
                        },
                        websocket,
                    )
                    continue

            finally:
                db.close()

            db = SessionLocal()

            try:
                answer = answer_service.submit_answer(
                    db,
                    message.question_id,
                    answer_text,
                )

            except Exception as exc:
                logger.exception(
                    "WebSocket answer submission failed | "
                    "interview_id=%s | "
                    "question_id=%s | "
                    "user_id=%s",
                    interview_id,
                    message.question_id,
                    user_id,
                )

                await manager.send_personal_message(
                    {
                        "event": WebSocketEvent.ERROR,
                        "data": {
                            "message": (
                                "Unable to submit answer."
                            ),
                        },
                    },
                    websocket,
                )
                continue

            finally:
                db.close()

            await manager.broadcast_event(
                WebSocketEvent.ANSWER_SUBMITTED,
                {
                    "interview_id": interview_id,
                    "user_id": user_id,
                    "answer_id": answer.id,
                },
                interview_id,
            )

            await manager.broadcast_event(
                WebSocketEvent.ANSWER_EVALUATED,
                {
                    "interview_id": interview_id,
                    "user_id": user_id,
                    "answer_id": answer.id,
                    "score": answer.score,
                    "feedback": answer.feedback,
                    "suggested_improvement": (
                        answer.suggested_improvement
                    ),
                },
                interview_id,
            )

    except WebSocketDisconnect:
        manager.disconnect(
            websocket,
            interview_id,
        )

    except Exception:
        logger.exception(
            "Unexpected WebSocket error | "
            "interview_id=%s | "
            "user_id=%s",
            interview_id,
            user_id,
        )

        manager.disconnect(
            websocket,
            interview_id,
        )

        try:
            await websocket.close(
                code=1011,
                reason="Internal WebSocket error.",
            )
        except Exception:
            pass