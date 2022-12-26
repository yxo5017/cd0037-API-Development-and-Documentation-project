import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
            "question":"test",
            "answer":"test",
            "difficulty": 2,
            "category": 2,
        }
        self.search_word = {
            "searchTerm": "Whose"
        }

        self.quiz_page = {
            "quiz_category": {
                "id":1
            }
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_paginated_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["categories"]))

    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get("/questions?page=1000")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["message"], "resource not found")

    def test_create_new_question(self):
        res = self.client().post("/questions", json=self.new_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    def test_405_if_question_not_created(self):
        res = self.client().post("/questions/45", json=self.new_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["message"], "method not allowed")

    def test_delete_question(self):
        res = self.client().delete("/questions/5")
        data = json.loads(res.data)
        question = Question.query.filter(Question.id == 5).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_422_if_book_does_not_exist(self):
        res = self.client().delete("questions/1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
    
    def test_get_category(self):
        res = self.client().get("/categories/1/questions")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data["questions"]))

    def test_not_get_categories(self):
        res = self.client().get("/categories/www/questions")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
 
    def test_search_quizzes(self):
        res = self.client().post("/questions/search", json=self.search_word)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    def test_not_search_quizzes(self):
        res = self.client().post("/questions/searchhh", json=self.search_word)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        
    def test_get_quiz_category(self):
        res = self.client().post("/quizzes", json=self.quiz_page)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        # assertsame, assertarray, ドキュメントと見比べる、カテゴリ数と付き合わせてチェックする

    def test_not_get_quiz_category(self):
        res = self.client().post("/quizzess", json=self.quiz_page)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()