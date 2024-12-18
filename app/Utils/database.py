from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import settings

# Database URL
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.DB_USERNAME}:{settings.DB_PASSWORD}@{settings.DB_URL}:{settings.DB_PORT}/{settings.DB_NAME}"

# Create the database engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a session local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for the database
Base = declarative_base()

# Dependency for Dependency Injection/Sessions
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()