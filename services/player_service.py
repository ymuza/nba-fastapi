import json

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from models import Player
import redis

redis_client = redis.Redis(host='localhost', port=6379, db=0)


class PlayerService:

    @staticmethod
    async def get_player_by_name(self, player_name: str, db: Session):
        cached_data = redis_client.get(f"player_name_{player_name}")
        if cached_data:  # check if data is cached
            return cached_data
        #if not cached, fetch from db
        player_model = db.query(Player).filter(Player.name == player_name).first()
        if player_model is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Player not found.")

        # serialize the player before caching, otherwise it will throw errors
        player_data = {
            "id": player_model.id,
            "name": player_model.name,
            "height": player_model.height,
            "weight": player_model.weight,
            "years_pro": player_model.years_pro,
            "age": player_model.age,
        }

        redis_client.set(f"player_name_{player_name}", json.dumps(player_data))  # cache the fetched data
        return player_model

    @staticmethod
    async def get_players_by_height(self, height: float, db: Session):
        cached_data = redis_client.get(f"players_by_height_{height}")
        if cached_data:
            return cached_data
        players_by_height = db.query(Player).filter(Player.height == height).all()
        if players_by_height is None:
            if not players_by_height:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="No players found for the given height.")
        #
        players_data = [{
            "name": player.name,
            "height": player.height,
            "age": player.age,
        } for player in players_by_height]

        redis_client.set(f"players_by_height_{height}", json.dumps(players_data))
        return players_by_height
