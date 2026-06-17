from sqlalchemy import Column, String, DateTime, ForeignKey
from datetime import datetime, UTC

from db.database import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"))
    action = Column(String)
    entity_type = Column(String)
    entity_id = Column(String)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC)
    )