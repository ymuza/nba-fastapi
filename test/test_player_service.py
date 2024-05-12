from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models import Player
from services.player_service import PlayerService


@pytest.fixture
def mock_db_session():
    return MagicMock(spec=Session)


@pytest.fixture
def player_service(mock_db_session):
    return PlayerService()


@pytest.mark.asyncio
async def test_get_player_by_name_found(player_service, mock_db_session):
    # Arrange
    player_name = "Test Player"
    expected_player_data = {
        "id": 1,
        "name": player_name,
        "height": 6.5,
        "weight": 200,
        "years_pro": 3,
        "age": 25,
    }
    mock_player_model = Player(**expected_player_data)
    mock_db_session.query().filter().first.return_value = mock_player_model

    # Act
    result = await player_service.get_player_by_name(player_name, mock_db_session)

    # Assert
    assert result.id == expected_player_data["id"]
    assert result.name == expected_player_data["name"]
    assert result.height == expected_player_data["height"]
    assert result.weight == expected_player_data["weight"]
    assert result.years_pro == expected_player_data["years_pro"]
    assert result.age == expected_player_data["age"]


@pytest.mark.asyncio
async def test_get_player_by_name_not_found(player_service, mock_db_session):
    # Arrange
    player_name = "Nonexistent Player"
    mock_db_session.query().filter().first.return_value = None

    # Act & Assert
    with pytest.raises(HTTPException) as exc_info:
        await player_service.get_player_by_name(player_name, mock_db_session)
    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    assert exc_info.value.detail == "player not found."
