from datetime import datetime, timedelta

from bs4 import BeautifulSoup

import server


class TestBook:
    def test_booking_with_unknown_club(self, monkeypatch, list_of_clubs, list_of_competitions, client):
        monkeypatch.setattr(target=server, name="clubs", value=list_of_clubs)
        monkeypatch.setattr(target=server, name="competitions", value=list_of_competitions)
        response = client.get(f"/book/{list_of_competitions[0]['name']}/unknown_club")
        response_data_html = BeautifulSoup(response.data, features="html.parser")
        error_message = response_data_html.find(name="p", class_="error").string
        assert error_message == "Sorry, you are not authorized to make this request."
        assert response.status_code == 401

    def test_booking_with_unknown_competition(self, monkeypatch, list_of_clubs, list_of_competitions, client):
        monkeypatch.setattr(target=server, name="clubs", value=list_of_clubs)
        monkeypatch.setattr(target=server, name="competitions", value=list_of_competitions)
        response = client.get(f"/book/unknown_competition/{list_of_clubs[0]['name']}")
        response_data_html = BeautifulSoup(response.data, features="html.parser")
        message = response_data_html.find(name="ul", class_="message")
        assert "Something went wrong-please try again" in str(message)
        assert response.status_code == 400

    def test_booking_an_old_competition(self, monkeypatch, list_of_clubs, list_of_competitions, client):
        monkeypatch.setattr(target=server, name="clubs", value=list_of_clubs)
        monkeypatch.setattr(target=server, name="competitions", value=list_of_competitions)
        monkeypatch.setitem(list_of_competitions[0], name="date", value="2000-01-01 11:00:00")
        response = client.get(f"/book/{list_of_competitions[0]['name']}/{list_of_clubs[0]['name']}")
        response_data_html = BeautifulSoup(response.data, features="html.parser")
        message = response_data_html.find(name="ul", class_="message")
        assert "This competition is already over." in str(message)
        assert response.status_code == 400

    def test_booking_a_future_competition(self, monkeypatch, list_of_clubs, list_of_competitions, client):
        monkeypatch.setattr(target=server, name="clubs", value=list_of_clubs)
        monkeypatch.setattr(target=server, name="competitions", value=list_of_competitions)
        tomorrow = (datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
        monkeypatch.setitem(list_of_competitions[0], name="date", value=tomorrow)
        response = client.get(f"/book/{list_of_competitions[0]['name']}/{list_of_clubs[0]['name']}")
        response_data_html = BeautifulSoup(response.data, features="html.parser")
        title = response_data_html.find("title").string
        assert f"Booking for {list_of_competitions[0]['name']}" in title
        assert response.status_code == 200
