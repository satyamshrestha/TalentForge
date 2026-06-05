from pydantic import BaseModel

class ResumeCreate(BaseModel):
    file_url: str
    parsed_text: str

class ResumeUpdate(BaseModel):
    file_url: str
    parsed_text: str

class ResumeResponse(BaseModel):
    id: str
    file_url: str
    parsed_text: str
    user_id: str

    class Config:
        from_attributes = True