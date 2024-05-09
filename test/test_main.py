from fastapi import status
from fastapi.testclient import TestClient

import main

client = TestClient(main.app)


def test_return_healthcheck():
    response = client.get("/healthy")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'status': 'healthy'}
