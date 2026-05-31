from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from db.database import Base

class Resume(Base):
    __tablename__ = "resumes"
    id = Column(String, primary_key=True)
    file_url = Column(String)
    parsed_text = Column(String)
    user_id = Column(
        String,
        ForeignKey("users.id")
    )
    user = relationship(
        "User",
        back_populates="resumes"
    )