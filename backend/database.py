import os
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base , sessionmaker

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL= os.getenv("OPENAI_MODEL")
SQLITE_URL = os.getenv("SQLITE_URL")

Base= declarative_base()
engine= create_engine(SQLITE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
