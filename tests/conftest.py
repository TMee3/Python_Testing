import pytest

from server import app


@pytest.fixture()
def client():
    app.config.from_object({"TESTING": True})
    with app.test_client() as client:
        yield client


@pytest.fixture()
def list_of_clubs():
    clubs = [
        {
            "name": "Test mail",
            "email": "good_mail@test.com",
            "points": "7"
        },
    ]
    return clubs


@pytest.fixture()
def list_of_competitions():
    competitions = [
        {
            "name": "Test competition",
            "date": "2024-01-01 11:00:00",
            "numberOfPlaces": "11"
        },
    ]
    return competitions
