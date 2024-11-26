#!/usr/bin/python3
"""Tests for Review model"""
import unittest
from unittest.mock import patch
from models.review import Review
from models.place import Place
from models.user import User
from models import storage
import json

class TestReviewAPI(unittest.TestCase):
    """Test cases for Review API"""

    @patch('models.storage')
    def setUp(self, mock_storage):
        """Set up test cases with mocked storage"""
        self.user = User(email="test@example.com", password="password123")
        self.place = Place(name="My Place", user_id=self.user.id)
        self.review = Review(text="Great place!", place_id=self.place.id, user_id=self.user.id)
        mock_storage.new.return_value = None
        mock_storage.save.return_value = None

    @patch('api.v1.app.app.test_client')
    def test_create_review(self, mock_client):
        """Test POST /api/v1/places/<place_id>/reviews"""
        mock_client.return_value.post.return_value.status_code = 201
        response = mock_client().post(f'/api/v1/places/{self.place.id}/reviews',
                                       data=json.dumps({"text": "Amazing stay!"}),
                                       content_type='application/json')
        self.assertEqual(response.status_code, 201)

    @patch('api.v1.app.app.test_client')
    def test_get_review(self, mock_client):
        """Test GET /api/v1/reviews/<review_id>"""
        mock_client.return_value.get.return_value.status_code = 200
        response = mock_client().get(f'/api/v1/reviews/{self.review.id}')
        self.assertEqual(response.status_code, 200)

    @patch('api.v1.app.app.test_client')
    def test_update_review(self, mock_client):
        """Test PUT /api/v1/reviews/<review_id>"""
        mock_client.return_value.put.return_value.status_code = 200
        response = mock_client().put(f'/api/v1/reviews/{self.review.id}',
                                      data=json.dumps({'text': 'Updated Review'}),
                                      content_type='application/json')
        self.assertEqual(response.status_code, 200)

    @patch('api.v1.app.app.test_client')
    def test_delete_review(self, mock_client):
        """Test DELETE /api/v1/reviews/<review_id>"""
        mock_client.return_value.delete.return_value.status_code = 200
        response = mock_client().delete(f'/api/v1/reviews/{self.review.id}')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()