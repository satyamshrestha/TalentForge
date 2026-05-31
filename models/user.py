from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from db.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    resumes = relationship(
        "Resume",
        back_populates="user"
    )
    interviews = relationship(
        "Interview",
        back_populates="user"
    )