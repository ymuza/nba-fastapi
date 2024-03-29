from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DTABASE_URL = "postgresql://yamil:32874993@localhost:5432/nba"

engine = create_engine(SQLALCHEMY_DTABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
