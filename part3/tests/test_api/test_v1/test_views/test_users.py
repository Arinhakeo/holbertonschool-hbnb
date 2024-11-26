#!/usr/bin/python3
"""Tests for User API"""
import unittest
from unittest.mock import patch
from flask import json
from api.v1.app import app
from models.user import User
from models import storage


class TestUserAPI(unittest.TestCase):
    """Test cases for User API"""

    def setUp(self):
        storage.rollback()
        """Set up the test client"""
        self.client = app.test_client()
        self.user_data = {
            "email": "test@example.com",
            "password": "password123",
            "first_name": "Test",
            "last_name": "User"
        }

        # Ajouter un utilisateur
        self.user = User(**self.user_data)
        self.user.id = "1234"
        storage.new(self.user)
        storage.save()

    def tearDown(self):
        """Nettoyer la base après chaque test"""
        storage.delete_all()
        storage.save()

    @patch('models.storage.all')
    def test_get_users(self, mock_storage_all):
        """Test GET /api/v1/users"""
        mock_storage_all.return_value = {"User.1234": self.user}

        response = self.client.get('/api/v1/users')
        self.assertEqual(response.status_code, 200)

        # Vérifier le contenu de la réponse
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["id"], "1234")
        self.assertEqual(data[0]["email"], self.user_data["email"])

    @patch('models.storage.get')
    def test_get_user_by_id(self, mock_storage_get):
        """Test GET /api/v1/users/<user_id>"""
        mock_storage_get.return_value = self.user

        response = self.client.get(f'/api/v1/users/{self.user.id}')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertEqual(data["id"], "1234")
        self.assertEqual(data["email"], self.user_data["email"])

    @patch('models.storage.new')
    @patch('models.storage.save')
    def test_create_user(self, mock_storage_save, mock_storage_new):
        """Test POST /api/v1/users"""
        response = self.client.post('/api/v1/users', data=json.dumps(self.user_data),
                                     content_type='application/json')
        self.assertEqual(response.status_code, 201)

        mock_storage_new.assert_called_once()
        mock_storage_save.assert_called_once()

        data = json.loads(response.data)
        self.assertEqual(data["email"], self.user_data["email"])

    @patch('models.storage.get')
    @patch('models.storage.save')
    def test_update_user(self, mock_storage_save, mock_storage_get):
        """Test PUT /api/v1/users/<user_id>"""
        mock_storage_get.return_value = self.user

        updated_data = {"first_name": "UpdatedName"}
        response = self.client.put(f'/api/v1/users/{self.user.id}', data=json.dumps(updated_data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)

        mock_storage_save.assert_called_once()

        data = json.loads(response.data)
        self.assertEqual(data["first_name"], "UpdatedName")

    @patch('models.storage.get')
    @patch('models.storage.delete')
    def test_delete_user(self, mock_storage_delete, mock_storage_get):
        """Test DELETE /api/v1/users/<user_id>"""
        mock_storage_get.return_value = self.user

        response = self.client.delete(f'/api/v1/users/{self.user.id}')
        self.assertEqual(response.status_code, 200)

        mock_storage_delete.assert_called_once()


if __name__ == '__main__':
    unittest.main()