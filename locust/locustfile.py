from locust import HttpUser, task, between


class LocustTest(HttpUser):
    wait_time = between(1, 3)

    @task
    def index(self):
        self.client.get("/")

    @task
    def competition_booking_url_is_online(self):
        self.client.get("/book/Spring%20Festival/Simply%20Lift")

    @task
    def booking_a_competition(self):
        self.client.post("/purchasePlaces", data={"places": "1",
                                                  "club": "Simply Lift",
                                                  "competition": "Spring Festival"
                                                  })

    @task
    def go_to_board(self):
        self.client.get("/board")

    def on_start(self):
        self.client.post("/showSummary", data={'email': 'john@simplylift.co'})

    def on_stop(self):
        self.client.get("/logout")

