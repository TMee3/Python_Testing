from bs4 import BeautifulSoup

import server


class TestLoginLogout:
    def test_login_logout(self, monkeypatch, list_of_clubs, client):
        monkeypatch.setattr(target=server, name="clubs", value=list_of_clubs)
        club = list_of_clubs[0]

        # The club accesses the login section.
        response = client.get("/")
        response_data_html = BeautifulSoup(response.data, features="html.parser")
        title = response_data_html.find("h1").string
        assert title == "Welcome to the GUDLFT Registration Portal!"
        assert response.status_code == 200

        # The club connects to the site.
        response = client.post("/showSummary", data={"email": club["email"]})
        response_data_html = BeautifulSoup(response.data, features="html.parser")
        title = response_data_html.find("h2").string
        assert f"Welcome, {club['email']}" in title
        assert response.status_code == 200

        # The club disconnects from the site.
        response = client.get("/logout")
        assert response.status_code == 302
        assert response.location == "/"
