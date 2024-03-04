from fastapi import FastAPI, Depends, HTTPException
from typing import Annotated, List

from sqlalchemy import or_
from sqlalchemy.orm import Session
from models import Team
import models
from database import engine, SessionLocal

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/teams_info")
async def read_all(db: Annotated[Session, Depends(get_db)]):
    return db.query(Team).all()
