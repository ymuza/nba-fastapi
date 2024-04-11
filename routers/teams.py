from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from starlette import status
from pydantic_models.teams import Team
from models import Teams
from database import get_db

router = APIRouter(
    prefix="/teams", tags=["teams"], responses={404: {"description": "not found"}}
)


@router.get("/{team_name}", status_code=status.HTTP_200_OK)
async def get_team_by_name(team_name: str, db: Session = Depends(get_db)):
    team_model = db.query(Teams).filter(Teams.name == team_name).first()
    if team_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
    return team_model


@router.delete("/{team_name}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_player(team_name: str, db: Session = Depends(get_db)):
    team_model = db.query(Teams).filter(Teams.name == team_name).first()
    if team_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
    db.delete(team_model)
    db.commit()
    return {"message": "Team deleted successfully"}


@router.put("{team_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_team(
        team_request: Team, db: Session = Depends(get_db), team_id: int = Path(gt=0)
):
    team_model = db.query(Teams).filter(Teams.id == team_id).first()
    if team_model is None:
        raise HTTPException(status_code=404, detail="team not found")

    team_model.city = team_request.city
    team_model.coach_id = team_request.coach_id

    db.add(team_model)
    db.commit()
