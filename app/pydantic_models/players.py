from pydantic import BaseModel, Field


class Players(BaseModel):
    name: str = Field(min_length=2)
    height: float = Field()
    weight: int = Field()
    years_pro: int = Field()
    birthdate: str = Field(min_length=6)
    age: int = Field()
    team_id: int = Field()
