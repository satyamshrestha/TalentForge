from pydantic import BaseModel

class ResumeResponse(BaseModel):
    id: str
    file_path: str
    parsed_text: dict | None
    status: str
    error_message: str | None
    user_id: str

    class Config:
        from_attributes = True