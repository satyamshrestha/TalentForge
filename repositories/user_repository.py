from sqlalchemy.orm import Session

from models.user import User

class UserRepository:

    def get_by_email(
        self,
        db: Session,
        email: str
    ):
        return (db.query(User).filter(User.email == email).first())
    
    def get_by_google_id(
        self,
        db: Session,
        google_id: str
    ):
        return (
            db.query(User)
            .filter(User.google_id == google_id)
            .first()
        )

    def get_by_id(
        self,
        db: Session,
        user_id: str
    ):
        return (
            db.query(User)
            .filter(User.id == user_id)
            .first()
        )

    def create_user(
        self,
        db: Session,
        user: User
    ):
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    def update_google_id(
        self,
        db: Session,
        user: User,
        google_id: str
    ):
        user.google_id = google_id
        db.commit()
        db.refresh(user)
        return user
    
    def commit_and_refresh(
        self,
        db: Session,
        user: User
    ):
        db.commit()
        db.refresh(user)