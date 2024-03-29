from pydantic import BaseModel, Field


class Team(BaseModel):
    name: str = Field(min_length=6)
    city: str = Field(min_length=4)
    coach_id: int = Field()
    assistant_coach_id: int = Field()
    manager_id: int = Field()
    owner_id: int = Field()
