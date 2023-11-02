from bs4 import BeautifulSoup

import server


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

    def test_purchase_place_by_not_entering_a_digit(self, monkeypatch, list_of_clubs, list_of_competitions, client):
        monkeypatch.setattr(target=server, name="clubs", value=list_of_clubs)
        monkeypatch.setattr(target=server, name="competitions", value=list_of_competitions)
        purchase_data = {
            "club": list_of_clubs[0]["name"],
            "competition": list_of_competitions[0]["name"],
            "places": "this is not a number",
        }
        response = client.post("/purchasePlaces", data=purchase_data)
        response_data_html = BeautifulSoup(response.data, features="html.parser")
        error_message = response_data_html.find(name="p", class_="error").string
        assert error_message == "Please enter a number between 1 and 12"
        assert response.status_code == 400

    def test_purchase_place_by_entering_zero(self, monkeypatch, list_of_clubs, list_of_competitions, client):
        monkeypatch.setattr(target=server, name="clubs", value=list_of_clubs)
        monkeypatch.setattr(target=server, name="competitions", value=list_of_competitions)
        purchase_data = {
            "club": list_of_clubs[0]["name"],
            "competition": list_of_competitions[0]["name"],
            "places": "0",
        }
        response = client.post("/purchasePlaces", data=purchase_data)
        response_data_html = BeautifulSoup(response.data, features="html.parser")
        error_message = response_data_html.find(name="p", class_="error").string
        assert error_message == "Please take between 1 and 12 places maximum."
        assert response.status_code == 400

    def test_purchase_place_by_entering_number_greater_than_twelve(self, monkeypatch, list_of_clubs,
                                                                   list_of_competitions, client):
        monkeypatch.setattr(target=server, name="clubs", value=list_of_clubs)
        monkeypatch.setattr(target=server, name="competitions", value=list_of_competitions)
        purchase_data = {
            "club": list_of_clubs[0]["name"],
            "competition": list_of_competitions[0]["name"],
            "places": "15",
        }
        response = client.post("/purchasePlaces", data=purchase_data)
        response_data_html = BeautifulSoup(response.data, features="html.parser")
        error_message = response_data_html.find(name="p", class_="error").string
        assert error_message == "Please take between 1 and 12 places maximum."
        assert response.status_code == 400

    def test_purchase_place_by_entering_number_greater_than_total_places(self, monkeypatch, list_of_clubs,
                                                                         list_of_competitions, client):
        monkeypatch.setattr(target=server, name="clubs", value=list_of_clubs)
        monkeypatch.setattr(target=server, name="competitions", value=list_of_competitions)
        purchase_data = {
            "club": list_of_clubs[0]["name"],
            "competition": list_of_competitions[0]["name"],
            "places": "12",
        }
        response = client.post("/purchasePlaces", data=purchase_data)
        response_data_html = BeautifulSoup(response.data, features="html.parser")
        error_message = response_data_html.find(name="p", class_="error").string
        assert error_message == (f"Sorry, there are not enough places left "
                                 f"({list_of_competitions[0]['numberOfPlaces']}).")
        assert response.status_code == 400

    def test_purchase_place_by_entering_number_between_one_and_twelve_include(self, monkeypatch, list_of_clubs,
                                                                              list_of_competitions, client):
        monkeypatch.setattr(target=server, name="clubs", value=list_of_clubs)
        monkeypatch.setattr(target=server, name="competitions", value=list_of_competitions)
        places_required = "8" if int(list_of_clubs[0]["points"]) > 12 else list_of_clubs[0]["points"]
        purchase_data = {
            "club": list_of_clubs[0]["name"],
            "competition": list_of_competitions[0]["name"],
            "places": places_required,
        }
        response = client.post("/purchasePlaces", data=purchase_data)
        response_data_html = BeautifulSoup(response.data, features="html.parser")
        validation_message = response_data_html.find(name="ul", class_="message")
        assert "Great-booking complete!" in str(validation_message)
        assert response.status_code == 200

    def test_update_club_points_after_booking_place(self, monkeypatch, list_of_clubs, list_of_competitions, client):
        monkeypatch.setattr(target=server, name="clubs", value=list_of_clubs)
        monkeypatch.setattr(target=server, name="competitions", value=list_of_competitions)
        old_club_points = int(list_of_clubs[0]["points"])
        places_required = "8" if int(list_of_clubs[0]["points"]) > 12 else list_of_clubs[0]["points"]
        purchase_data = {
            "club": list_of_clubs[0]["name"],
            "competition": list_of_competitions[0]["name"],
            "places": places_required,
        }
        response = client.post("/purchasePlaces", data=purchase_data)
        response_data_html = BeautifulSoup(response.data, features="html.parser")
        club_points_message = response_data_html.find(name="p", class_="club_points").string
        assert club_points_message == f"Points available: {old_club_points - int(places_required)}"
        assert response.status_code == 200
