from bs4 import BeautifulSoup
import server
from tests.conftest import client, list_of_clubs
import pytest

class TestLogin:
    GOOD_EMAIL = "good_mail@test.com"
    UNKNOWN_EMAIL = "unknown_mail@test.com"

    def setUp(self):
        self.client = client
        self.list_of_clubs = list_of_clubs

    def send_post_request_and_check_title(self, email, expected_title):
        response = self.client.post("/showSummary", data={"email": email})
        response_data_html = BeautifulSoup(response.data, features="html.parser")
        title = response_data_html.find("title").string
        assert expected_title in title
        assert response.request.path == "/showSummary"
        assert response.status_code == 200

    @pytest.mark.parametrize("email, expected_title", [
        ("good_mail@test.com", "Summary"),
        ("unknown_mail@test.com", "Sorry, that email wasn't found.")
    ])
    def test_login(self, monkeypatch, email, expected_title):
        monkeypatch.setattr(target=server, name="clubs", value=self.list_of_clubs)
        self.send_post_request_and_check_title(email, expected_title)
