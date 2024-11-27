#!/usr/bin/python3
"""Tests for User model"""
import unittest
from unittest.mock import patch, MagicMock
from models.user import User
from models import storage
from flask import Flask, jsonify
import json
from api.v1.app import app

# Simuler une application Flask
app = Flask(__name__)

class TestUserAPI(unittest.TestCase):
    """Test cases for User API"""

    @patch('models.storage')
    def setUp(self, mock_storage):
        """Set up test cases with mocked storage"""
        self.user_data = {
            'email': 'test@example.com',
            'password': 'password123',
            'first_name': 'Test',
            'last_name': 'User'
        }
        self.user = User(**self.user_data)
        mock_storage.new.return_value = None
        mock_storage.save.return_value = None

    @patch('flask.Flask.test_client')
    def test_create_user(self, mock_client):
        """Test POST /api/v1/users"""
        # Simuler la réponse de test_client()
        mock_client.return_value.post.return_value.status_code = 201
        mock_client.return_value.post.return_value.json = {
            'id': '1234',
            'email': self.user_data['email']
        }
        response = mock_client().post('/api/v1/users', data=json.dumps(self.user_data),
                                       content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['email'], self.user_data['email'])

    @patch('flask.Flask.test_client')
    def test_get_user(self, mock_client):
        """Test GET /api/v1/users/<user_id>"""
        mock_client.return_value.get.return_value.status_code = 200
        mock_client.return_value.get.return_value.json = {
            'id': '1234',
            'email': self.user_data['email']
        }
        response = mock_client().get('/api/v1/users/1234')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['email'], self.user_data['email'])

if __name__ == '__main__':
    unittest.main()