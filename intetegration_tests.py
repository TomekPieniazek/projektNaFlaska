import unittest
import json
from main import app
from Resources import *
import pytest

class FlaskIntegrationTest(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_get_users(self):
        response = self.app.get('/users')
        self.assertEqual(response.status_code, 200)

    def test_get_user_by_id(self):
        response = self.app.get('/users/1')
        self.assertEqual(response.status_code, 200)

    def test_add_users(self):
        new_user = {"name": "Test_Integracyjny", "lastname": "test_h"}
        response = self.app.post('/users', json=new_user)
        self.assertEqual(response, 201)

    def test_change_user(self):
        new_update_user = {"name": "Test_Integracyjny11111", "lastname": "test_h1111"}
        response = self.app.patch('/users/1', json=new_update_user)
        self.assertEqual(response, 204)

    def test_add_user(self):
        new_update_user = {"name": "Test_Integracyjny11111", "lastname": "test_h1111"}
        response = self.app.put('/users/1', json=new_update_user)
        self.assertEqual(response, 204)

    def test_delete_user(self):
        response = self.app.delete('/users/1')
        self.assertEqual(response, 204)


if __name__ == '__main__':
    unittest.main()



