from pydantic import BaseModel, Field


class WebSocketAnswerMessage(BaseModel):
    question_id: str
    answer: str = Field(
        min_length=1,
        max_length=10000,
    )