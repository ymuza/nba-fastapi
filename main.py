from fastapi import FastAPI

from database import SessionLocal, engine
from models import Base
from routers import players, teams

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/healthy")  # api healthcheck
def health_check():
    return {'status': 'healthy'}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app.include_router(players.router)
app.include_router(teams.router)
