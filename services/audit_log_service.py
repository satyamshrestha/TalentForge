import uuid

from sqlalchemy.orm import Session

from models.audit_log import AuditLog
from repositories.audit_log_repository import AuditLogRepository


class AuditLogService:

    def __init__(
        self,
        audit_log_repository: AuditLogRepository
    ):
        self.audit_log_repository = audit_log_repository

    def log_action(
        self,
        db: Session,
        user_id: str,
        action: str,
        entity_type: str,
        entity_id: str
    ):
        audit_log = AuditLog(
            id=str(uuid.uuid4()),
            user_id=user_id,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id
        )

        return self.audit_log_repository.create_log(db, audit_log)