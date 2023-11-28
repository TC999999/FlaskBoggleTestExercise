from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle

app.config["TESTING"] = True


class FlaskTests(TestCase):
    # TODO -- write tests for every view function / feature!
    def test_page_load(self):
        with app.test_client() as client:
            resp = client.get("/")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1><i>BOGGLE!</i></h1>", html)

    def test_word_submit(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session["board"] = Boggle().make_board()
                change_session["player_score"] = ["red", "blue", "yellow"]

            resp = client.post("/checking", json={"json": {"wordData": "hfhfhfhfh"}})
            resp2 = client.post("/checking", json={"json": {"wordData": "green"}})
            result = resp.get_data(as_text=True)
            result2 = resp2.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertEqual("not-word", result)
            if result2 == "not-on-board":
                self.assertEqual("not-on-board", result2)
            else:
                self.assertEqual("ok", result2)

    def test_reset(self):
        with app.test_client() as client:
            resp = client.get("/reset")

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, "/")

    def test_reset_followed(self):
        with app.test_client() as client:
            resp = client.get("/reset", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1><i>BOGGLE!</i></h1>", html)

    def test_session_info(self):
        with app.test_client() as client:
            resp = client.get("/count")

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(session["count"], 1)

    def test_session_info_set(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session["count"] = 99

            resp = client.get("/count")

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(session["count"], 100)

    def test_results(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session["result"] = "ok"

            resp = client.get("/results/json")
            result = resp.get_json()
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(result, {"result": "ok"})

    def test_score(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session["player_score"] = ["red", "blue", "yellow"]
            resp = client.get("/score")
            score = resp.get_json()

            self.assertEqual(resp.status_code, 200)
            self.assertTrue(type(score) is list)

    def test_high_score(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session["player_high_score"] = 30

            resp = client.post("/high_score", json={"json": {"total": 20}})
            score = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(session["player_high_score"], 30)

    def test_high_score_2(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session["player_high_score"] = 30

            resp = client.post("/high_score", json={"json": {"total": 40}})
            score = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(session["player_high_score"], 40)
