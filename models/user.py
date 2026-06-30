from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from db.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, default="student", nullable=False)
    provider = Column(String, nullable=False, default="local")
    resumes = relationship(
        "Resume",
        back_populates="user"
    )
    interviews = relationship(
        "Interview",
        back_populates="user"
    )