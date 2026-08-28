from pydantic import BaseModel, Field


class WebSocketAnswerMessage(BaseModel):
    question_id: str = Field(min_length=1)
    answer: str = Field(min_length=1)