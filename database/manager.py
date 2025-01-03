from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import get_database_url
from database.models import Base

DATABASE_URL = get_database_url()

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """
    Initialize the database: create tables if they don't exist.
    """
    Base.metadata.create_all(bind=engine)

def get_db():
    """
    Dependency to provide database sessions.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
