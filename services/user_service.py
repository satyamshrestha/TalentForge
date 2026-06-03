import uuid
from sqlalchemy.orm import Session

from auth.hashing import hash_password
from models.user import User
from repositories.user_repository import UserRepository

class UserService:
    def __init__(
        self,
        repository: UserRepository
    ):
        self.repository = repository

    def signup(
        self,
        db: Session,
        email: str,
        password: str
    ):
        existing_user = self.repository.get_by_email(db, email)
        if existing_user:
            raise ValueError("User already exists")

        user = User(
            id=str(uuid.uuid4()),
            email=email,
            password=hash_password(password)
        )
        return self.repository.create_user(db, user)