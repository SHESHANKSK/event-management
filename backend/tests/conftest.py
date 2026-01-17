import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.infrastructure.persistence.database import Base
from app.infrastructure.persistence.repositories import SqlAlchemyEventRepository, SqlAlchemyUserRepository

# Use in-memory SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture
def db_session():
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def event_repo(db_session):
    return SqlAlchemyEventRepository(db_session)

@pytest.fixture
def user_repo(db_session):
    return SqlAlchemyUserRepository(db_session)
