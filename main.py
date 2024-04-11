
from fastapi import  FastAPI


from routers import players, teams
import models
from database import SessionLocal, engine


app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app.include_router(players.router)
app.include_router(teams.router)
