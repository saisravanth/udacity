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
        self.database_path = "postgres://{}:{}@{}/{}".format('postgres', 'saisra246','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

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
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data['categories']), 6) 

    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['total_questions'], 20)
        self.assertEqual(len(data['categories']), 6)      

    def test_create_question(self):
        res = self.client().post('/questions', json={'question': 'Where is Burj Khalifa located ?', 'answer': 'Dubai', 'difficulty': 2, 'category': 3})
        self.assertEqual(res.status_code, 200)

    def test_remove_question_by_id(self):
        res = self.client().delete('/questions/27')
        self.assertEqual(res.status_code, 200)     

    def test_get_questions_by_search(self):
        res = self.client().post('/questions/tom')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data['questions']), 1)        

    def test_get_questions_by_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data['questions']), 3)        

    def test_get_random_questions(self):
        res = self.client().post('/quizzes', json={'quiz_category': {'id':1}, 'previous_questions': [20,21]})
        print("response:", json.loads(res.data))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['question']['id'], 22)
        
    def test_error_404(self):
        res = self.client().post('/questions/madagascar')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEquals(data['message'], 'Not found')
         
    def test_error_503(self):
        res = self.client().post('/quizzes', json={'quiz_category': {'id':1}, 'previous_questions': [20,21,22]})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 503)
        self.assertEquals(data['message'], 'We are out of questions !!')     

    def test_error_405(self):
        res = self.client().patch('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEquals(data['message'], 'Method not allowed') 


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()