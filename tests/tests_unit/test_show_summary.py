from bs4 import BeautifulSoup

import server
from tests.conftest import client, list_of_clubs


class TestLogin:
    GOOD_EMAIL = "good_mail@test.com"
    UNKNOWN_EMAIL = "unknown_mail@test.com"

    def test_login_with_good_email(self, monkeypatch, list_of_clubs, client):
        monkeypatch.setattr(target=server, name="clubs", value=list_of_clubs)
        response = client.post("/showSummary", data={"email": self.GOOD_EMAIL})
        response_data_html = BeautifulSoup(response.data, features="html.parser")
        title = response_data_html.find("title").string
        assert "Summary" in title
        assert response.request.path == "/showSummary"
        assert response.status_code == 200

    def test_login_with_unknown_email(self, monkeypatch, list_of_clubs, client):
        monkeypatch.setattr(target=server, name="clubs", value=list_of_clubs)
        response = client.post("/showSummary", data={"email": self.UNKNOWN_EMAIL})
        response_data_html = BeautifulSoup(response.data, features="html.parser")
        error_message = response_data_html.find(name="p", class_="error").string
        assert error_message == "Sorry, that email wasn't found."
        assert response.status_code == 401
