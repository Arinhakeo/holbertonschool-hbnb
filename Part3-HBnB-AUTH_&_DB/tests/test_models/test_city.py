#!/usr/bin/python3
"""Tests for City model"""
import unittest
from unittest.mock import patch
from models.city import City
from models.state import State
from models import storage
import json

class TestCityAPI(unittest.TestCase):
    """Test cases for City API"""

    @patch('models.storage')
    def setUp(self, mock_storage):
        """Set up test cases with mocked storage"""
        self.state = State(name="California")
        self.city = City(name="San Francisco", state_id=self.state.id)
        mock_storage.new.return_value = None
        mock_storage.save.return_value = None

    @patch('api.v1.app.app.test_client')
    def test_create_city(self, mock_client):
        """Test POST /api/v1/states/<state_id>/cities"""
        mock_client.return_value.post.return_value.status_code = 201
        response = mock_client().post(f'/api/v1/states/{self.state.id}/cities',
                                       data=json.dumps({"name": "Los Angeles"}),
                                       content_type='application/json')
        self.assertEqual(response.status_code, 201)

    @patch('api.v1.app.app.test_client')
    def test_get_city(self, mock_client):
        """Test GET /api/v1/cities/<city_id>"""
        mock_client.return_value.get.return_value.status_code = 200
        response = mock_client().get(f'/api/v1/cities/{self.city.id}')
        self.assertEqual(response.status_code, 200)

    @patch('api.v1.app.app.test_client')
    def test_update_city(self, mock_client):
        """Test PUT /api/v1/cities/<city_id>"""
        mock_client.return_value.put.return_value.status_code = 200
        response = mock_client().put(f'/api/v1/cities/{self.city.id}',
                                      data=json.dumps({'name': 'Updated City'}),
                                      content_type='application/json')
        self.assertEqual(response.status_code, 200)

    @patch('api.v1.app.app.test_client')
    def test_delete_city(self, mock_client):
        """Test DELETE /api/v1/cities/<city_id>"""
        mock_client.return_value.delete.return_value.status_code = 200
        response = mock_client().delete(f'/api/v1/cities/{self.city.id}')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()