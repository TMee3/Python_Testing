from bs4 import BeautifulSoup

import server


class TestGetListOfClubs:
    def test_display_clubs_points(self, monkeypatch, list_of_clubs, client):
        monkeypatch.setattr(target=server, name="clubs", value=list_of_clubs)
        response = client.get("/clubs")
        response_data_html = BeautifulSoup(response.data, features="html.parser")
        clubs_list = response_data_html.find("ul")
        assert f"Current points balance: {list_of_clubs[0]['points']}" in str(clubs_list)
        assert response.status_code == 200

    def test_display_clubs_name(self, monkeypatch, list_of_clubs, client):
        monkeypatch.setattr(target=server, name="clubs", value=list_of_clubs)
        response = client.get("/clubs")
        response_data_html = BeautifulSoup(response.data, features="html.parser")
        clubs_list = response_data_html.find("ul")
        assert f"{list_of_clubs[0]['name']}" in str(clubs_list)
        assert response.status_code == 200


class TestClubsEndpointMethod:
    FAKE_DATA = {"test": "fake data"}

    def test_clubs_post_not_allow(self, monkeypatch, list_of_clubs, client):
        monkeypatch.setattr(target=server, name="clubs", value=list_of_clubs)
        response = client.post("/clubs", data=self.FAKE_DATA)
        assert response.status_code == 405

    def test_clubs_put_not_allow(self, monkeypatch, list_of_clubs, client):
        monkeypatch.setattr(target=server, name="clubs", value=list_of_clubs)
        response = client.put("/clubs", data=self.FAKE_DATA)
        assert response.status_code == 405

    def test_clubs_patch_not_allow(self, monkeypatch, list_of_clubs, client):
        monkeypatch.setattr(target=server, name="clubs", value=list_of_clubs)
        response = client.patch("/clubs", data=self.FAKE_DATA)
        assert response.status_code == 405

    def test_clubs_delete_not_allow(self, monkeypatch, list_of_clubs, client):
        monkeypatch.setattr(target=server, name="clubs", value=list_of_clubs)
        response = client.delete("/clubs")
        assert response.status_code == 405
