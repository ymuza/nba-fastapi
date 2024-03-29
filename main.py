from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Path
from sqlalchemy.orm import Session
from starlette import status

import models
from database import SessionLocal, engine
from models import Player, Teams
from pydantic_models.players import Players
from pydantic_models.teams import Team

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/teams_info")
async def get_all_teams_info(db: db_dependency):
    return db.query(Teams).all()


@app.get("/teams/{team_city}", status_code=status.HTTP_200_OK)
async def get_players_by_team(db: db_dependency, team_city: str):
    nba_model = db.query(Teams).filter(Teams.city == team_city).all()
    if nba_model is not None:
        return nba_model
    raise HTTPException(status_code=404, detail="team not found")


@app.post("/players", status_code=status.HTTP_201_CREATED)
async def add_player(db: db_dependency, player_request: Players):
    players_model = Player(**player_request.dict())

    db.add(players_model)
    db.commit()


@app.post("/teams", status_code=status.HTTP_201_CREATED)
async def add_team(db: db_dependency, team_request: Team):
    teams_model = Teams(**team_request.dict())

    db.add(teams_model)
    db.commit()


@app.put("/teams/{team_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_team(
        db: db_dependency, team_request: Team, team_id: int = Path(gt=0)
):
    team_model = db.query(Team).filter(Team.id == team_id).first()
    if team_model is None:
        raise HTTPException(status_code=404, detail="team not found")

    team_model.city = team_request.city
    team_model.coach_id = team_request.coach_id

    db.add(team_model)
    db.commit()


@app.delete("/players/{player_name}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_player(db: db_dependency, player_name: str):
    player_model = db.query(Player).filter(Player.name == player_name).first()
    if player_model is None:
        raise HTTPException(status_code=404, detail="player not found")

    db.query(Player).filter(Player.name == player_name).delete()
    db.commit()
