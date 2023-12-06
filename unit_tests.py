import unittest
from unittest.mock import mock_open, patch
from main import app
from Resources import load_json, get_json, find_first_free_id, insert_user, update_user, delete_user

class TestFunctions(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_load_json(self):
        with patch('builtins.open', new_callable=mock_open, read_data='[{"id": 1, "name": "Test", "lastname": "Doe"}]'):
            data = load_json()
            assert data == [{"id": 1, "name": "Test", "lastname": "Doe"}]

    def test_find_first_free_id(self) -> None:
        with patch('functions.load_json', return_value=[{"id": 1}, {"id": 3}, {"id": 5}]):
            first_free_id = find_first_free_id()
            assert first_free_id == 2

    def test_insert_user(self) -> None:
        request_data = {'json': {'name': 'Test', 'lastname': 'Doe'}}

        with app.test_request_context('/users', json=request_data['json']):
            with patch('functions.load_json', return_value=[]):
                with patch('functions.find_first_free_id', return_value=1):
                    response = insert_user(request_data['json'])
                    assert response[1] == 201

    def test_update_user(self) -> None:
        user_id = 1
        updated_name = 'UpdatedName'
        request_data = {'json': {'name': updated_name}}

        with app.test_request_context(f'/users/{user_id}', json=request_data['json']):
            with patch('functions.load_json', return_value=[{"id": 1, "name": "Test", "lastname": "Doe"}]):
                response = update_user(user_id)
                assert response[1] == 204

    def test_delete_user(self) -> None:
        user_id = 1

        with app.test_request_context(f'/users/{user_id}'):
            with patch('functions.load_json', return_value=[{"id": 1, "name": "Test", "lastname": "Tests"}]):
                response = delete_user(user_id)
                assert response[1] == 204

if __name__ == '__main__':
    unittest.main()
