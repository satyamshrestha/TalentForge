from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, UTC

from db.database import Base

class Interview(Base):
    __tablename__ = "interviews"
    id = Column(String, primary_key=True)
    role_target = Column(String)
    status = Column(String)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    user_id = Column(String, ForeignKey("users.id"))
    user = relationship(
        "User",
        back_populates="interviews"
    )
    questions = relationship(
        "Question",
        back_populates="interview"
    )