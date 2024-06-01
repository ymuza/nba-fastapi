import json

import redis
from fastapi import HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from starlette import status

from app.models import Player

redis_client = redis.Redis(host="localhost", port=6379, db=0)


class PlayerService:

    async def get_player_by_name(self, player_name: str, db: Session):

        # cached_data = redis_client.get(f"player_name_{player_name}")
        # if cached_data:  # check if data is cached
        #     return cached_data

        # if not cached, fetch from db
        player_model = db.query(Player).filter(Player.name == player_name).first()
        if not player_model:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="player not found."
            )
        # serialize the player before caching, otherwise it will throw errors
        player_data = {
            "id": player_model.id,
            "name": player_model.name,
            "height": player_model.height,
            "weight": player_model.weight,
            "years_pro": player_model.years_pro,
            "age": player_model.age,
        }
        # redis_client.set(f"player_name_{player_name}", json.dumps(player_data))  # cache the fetched data

        return player_model

    async def get_players_by_height(self, height: float, db: Session):
        cached_data = redis_client.get(f"players_by_height_{height}")
        if cached_data:
            return cached_data
        players_by_height = db.query(Player).filter(Player.height == height).all()

        if not players_by_height:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No players found for the given height.",
            )

        players_data = [
            {
                "name": player.name,
                "height": player.height,
                "age": player.age,
            }
            for player in players_by_height
        ]

        redis_client.set(f"players_by_height_{height}", json.dumps(players_data))
        return players_by_height

    async def calculate_players_height_average(self, db: Session):
        cached_data = redis_client.get(f"players_height_average")
        if cached_data:
            return cached_data
        try:
            height_average = text("SELECT AVG(height) AS average_height FROM players")
            result = db.execute(height_average)
            average = result.fetchone()[0]
            print(average)

            if average is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="no players found for the avg.",
                )

            redis_client.set(
                f"players_height_average", json.dumps({"average": average})
            )
            return average
        except Exception as e:
            return {"error": str(e)}
