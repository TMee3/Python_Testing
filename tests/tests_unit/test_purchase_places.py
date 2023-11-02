from bs4 import BeautifulSoup

import server
from tests.conftest import client, list_of_clubs


class TestPurchasePlaces:
    def test_purchase_place_with_available_points(self, monkeypatch, list_of_clubs, list_of_competitions, client):
        monkeypatch.setattr(target=server, name="clubs", value=list_of_clubs)
        monkeypatch.setattr(target=server, name="competitions", value=list_of_competitions)
        purchase_data = {
            "club": list_of_clubs[0]["name"],
            "competition": list_of_competitions[0]["name"],
            "places": str(int(list_of_clubs[0]["points"]) - 1),
        }
        response = client.post("/purchasePlaces", data=purchase_data)
        response_data_html = BeautifulSoup(response.data, features="html.parser")
        title = response_data_html.find("title").string
        validation_message = response_data_html.find(name="ul", class_="message")
        assert "Summary" in title
        assert "Great-booking complete!" in str(validation_message)
        assert response.status_code == 200

    def test_purchase_place_with_too_much_points(self, monkeypatch, list_of_clubs, list_of_competitions, client):
        monkeypatch.setattr(target=server, name="clubs", value=list_of_clubs)
        monkeypatch.setattr(target=server, name="competitions", value=list_of_competitions)
        purchase_data = {
            "club": list_of_clubs[0]["name"],
            "competition": list_of_competitions[0]["name"],
            "places": str(int(list_of_clubs[0]["points"]) + 1),
        }
        response = client.post("/purchasePlaces", data=purchase_data)
        response_data_html = BeautifulSoup(response.data, features="html.parser")
        error_message = response_data_html.find(name="p", class_="error").string
        assert error_message == f"You don't have enough points (balance={list_of_clubs[0]['points']} points)."
        assert response.status_code == 400
