from datetime import datetime, timedelta

from bs4 import BeautifulSoup

import server


class TestBookingPlaces:
    def test_booking_places_process(self, monkeypatch, list_of_clubs, list_of_competitions, client):
        tomorrow = (datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
        competition_places = 15
        monkeypatch.setattr(target=server, name="clubs", value=list_of_clubs)
        monkeypatch.setattr(target=server, name="competitions", value=list_of_competitions)
        monkeypatch.setitem(list_of_competitions[0], name="date", value=tomorrow)
        monkeypatch.setitem(list_of_competitions[0], name="numberOfPlaces", value=str(competition_places))
        club = list_of_clubs[0]
        old_club_points = int(club["points"])
        competition = list_of_competitions[0]

        # The club selects a future competition
        response = client.get(f"/book/{competition['name']}/{club['name']}")
        response_data_html = BeautifulSoup(response.data, features="html.parser")
        title = response_data_html.find("h2").string
        assert f"{competition['name']}" in title
        assert response.status_code == 200

        # The club reserves places with its points
        places_required = "8" if int(club["points"]) > 12 else club["points"]
        purchase_data = {
            "club": club["name"],
            "competition": competition["name"],
            "places": places_required,
        }
        response = client.post("/purchasePlaces", data=purchase_data)
        response_data_html = BeautifulSoup(response.data, features="html.parser")
        validation_message = response_data_html.find(name="ul", class_="message")
        competitions_list = response_data_html.find_all(name="ul")
        club_points_message = response_data_html.find(name="p", class_="club_points").string
        assert "Great-booking complete!" in str(validation_message)
        assert response.status_code == 200
        assert f"Number of Places: {competition_places - int(places_required)}" in str(competitions_list)
        assert club_points_message == f"Points available: {old_club_points - int(places_required)}"
