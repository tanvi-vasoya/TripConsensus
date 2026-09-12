from collections.abc import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from app.config import settings

#This code sets up a database connection layer using SQLAlchemy 2.0. It is designed to automatically manage opening, using, and closing database connections for every individual web request.
engine = create_engine(
    settings.database_url,
    echo=settings.debug,
)
## CREATE A SESSION OBJECT TO INITIATE QUERY 
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,  #Stops SQLAlchemy from sending data to the database before you explicitly ask it to.
    expire_on_commit=False,
)
#combines table definition and class mapping into a single, unified syntax using a base class.
class Base(DeclarativeBase):
    """Base class for all SQLAlchemy ORM models."""
    pass
#get_db method to create database sessions when needed.
def get_db() -> Generator[Session, None, None]:
    """Create a new database session for each request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
