from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.DB_USERNAME}:{settings.DB_PASSWORD}@{settings.DB_URL}:{settings.DB_PORT}/{settings.DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency for Dependency Injection/Sessions
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()