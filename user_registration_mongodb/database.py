from pydantic import BaseSettings
from pymongo import MongoClient
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Connect to MongoDB

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Connect to MongoDB

class Settings(BaseSettings):
    app_name: str
    mongo_url: str

    class Config:
        env_file = ".env"


MongoClient = MongoClient(Settings.mongo_url)
db = MongoClient.UserData;
