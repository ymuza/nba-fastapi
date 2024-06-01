from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.database import get_db
from app.models import Player
from app.pydantic_models.players import Players
from app.services import player_service

router = APIRouter(
    prefix="/players", tags=["players"], responses={404: {"description": "not found"}}
)

p_service = player_service.PlayerService()

db_dependency = Annotated[Session, Depends(get_db)]


@router.get("/by_name/{player_name}", status_code=status.HTTP_200_OK)
async def get_player_by_his_name(player_name: str, db: db_dependency):
    player = await p_service.get_player_by_name(player_name, db)
    return player


@router.get("/by_height/{height}", status_code=status.HTTP_200_OK)
async def get_player_by_height(height: float, db: Session = Depends(get_db)):
    players = await p_service.get_players_by_height(height, db)
    return players


@router.get("/test", status_code=status.HTTP_200_OK)
async def test_function():
    print("test function - ssssssss")
    return 2 + 2


@router.get("/height_average", status_code=status.HTTP_200_OK)
async def get_players_height_average(db: Session = Depends(get_db)):
    height_average = await p_service.calculate_players_height_average(db)
    return height_average


@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_player(player_request: Players, db: Session = Depends(get_db)):
    player_model = Player(**player_request.dict())
    db.add(player_model)
    db.commit()
    return {"message": "Player added successfully"}


@router.delete("/{player_name}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_player(player_name: str, db: Session = Depends(get_db)):
    player_model = db.query(Player).filter(Player.name == player_name).first()
    if player_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="player not found")
    db.delete(player_model)
    db.commit()
    return {"message": "Player deleted successfully"}
