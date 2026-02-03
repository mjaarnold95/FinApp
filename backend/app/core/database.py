from sqlmodel import create_engine, SQLModel, Session

from .config import settings

# Create database engine
engine = create_engine(settings.database_url, echo=True)


def create_db_and_tables():
    """Create database tables"""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Get database session"""
    with Session(engine) as session:
        yield session
