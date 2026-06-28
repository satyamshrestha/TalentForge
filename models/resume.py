from sqlalchemy import Column, String, JSON, ForeignKey
from sqlalchemy.orm import relationship

from db.database import Base

class Resume(Base):
    __tablename__ = "resumes"
    id = Column(String, primary_key=True)
    file_path = Column(String, nullable=False)
    parsed_text = Column(JSON, nullable=True)
    status = Column(String, nullable=False, default="PENDING") #PENDING | PROCESSING | COMPLETED | FAILED
    error_message = Column(String, nullable=True)
    user_id = Column(String, ForeignKey("users.id"))
    user = relationship(
        "User",
        back_populates="resumes"
    )