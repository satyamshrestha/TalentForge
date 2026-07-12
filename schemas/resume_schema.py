from pydantic import BaseModel, ConfigDict

class ResumeResponse(BaseModel):
    id: str
    file_path: str
    parsed_text: dict | None
    status: str
    error_message: str | None
    user_id: str

    model_config = ConfigDict(
        from_attributes=True
    )