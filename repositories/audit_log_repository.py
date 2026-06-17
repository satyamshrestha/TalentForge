from sqlalchemy.orm import Session

from models.audit_log import AuditLog

class AuditLogRepository:

    def create_log(
        self,
        db: Session,
        audit_log: AuditLog
    ):
        db.add(audit_log)
        db.commit()
        db.refresh(audit_log)
        return audit_log