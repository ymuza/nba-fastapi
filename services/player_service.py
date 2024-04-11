from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from database import get_db
from models import Player


class PlayerService:

    async def get_player_by_name(self, player_name: str, db: Session):
        player_model = db.query(Player).filter(Player.name == player_name).first()
        if player_model is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Player not found.")
        return player_model

    async def get_players_by_height(self, height: float, db: Session):
        players = db.query(Player).filter(Player.height == height).all()
        if players is not None:
            return players
