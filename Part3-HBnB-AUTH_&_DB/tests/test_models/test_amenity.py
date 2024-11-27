#!/usr/bin/python3
"""Tests for Amenity model"""
import unittest
from unittest.mock import patch
from models.amenity import Amenity
from models import storage
import json
from flask import Flask
app = Flask(__name__)

class TestAmenityAPI(unittest.TestCase):
    """Test cases for Amenity API"""

    @patch('models.storage')
    def setUp(self, mock_storage):
        """Set up test cases with mocked storage"""
        self.amenity_data = {'name': 'WiFi'}
        self.amenity = Amenity(**self.amenity_data)
        mock_storage.new.return_value = None
        mock_storage.save.return_value = None

    @patch('api.v1.app.app.test_client')
    def test_create_amenity(self, mock_client):
        """Test POST /api/v1/amenities"""
        mock_client.return_value.post.return_value.status_code = 201
        response = mock_client().post('/api/v1/amenities', data=json.dumps(self.amenity_data),
                                       content_type='application/json')
        self.assertEqual(response.status_code, 201)

    @patch('api.v1.app.app.test_client')
    def test_get_amenity(self, mock_client):
        """Test GET /api/v1/amenities/<amenity_id>"""
        mock_client.return_value.get.return_value.status_code = 200
        response = mock_client().get(f'/api/v1/amenities/{self.amenity.id}')
        self.assertEqual(response.status_code, 200)

    @patch('api.v1.app.app.test_client')
    def test_update_amenity(self, mock_client):
        """Test PUT /api/v1/amenities/<amenity_id>"""
        mock_client.return_value.put.return_value.status_code = 200
        response = mock_client().put(f'/api/v1/amenities/{self.amenity.id}',
                                      data=json.dumps({'name': 'Updated WiFi'}),
                                      content_type='application/json')
        self.assertEqual(response.status_code, 200)

    @patch('api.v1.app.app.test_client')
    def test_delete_amenity(self, mock_client):
        """Test DELETE /api/v1/amenities/<amenity_id>"""
        mock_client.return_value.delete.return_value.status_code = 200
        response = mock_client().delete(f'/api/v1/amenities/{self.amenity.id}')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()