import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import models

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import app
from db.database import Base
from db.deps import get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

Base.metadata.create_all(bind=engine)