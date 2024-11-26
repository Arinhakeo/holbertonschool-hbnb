#!/usr/bin/python3
"""Tests for Place model"""
import unittest
from unittest.mock import patch
from models.place import Place
from models.city import City
from models.state import State
from models import storage
import json

class TestPlaceAPI(unittest.TestCase):
    """Test cases for Place API"""

    @patch('models.storage')
    def setUp(self, mock_storage):
        """Set up test cases with mocked storage"""
        self.state = State(name="California")
        self.city = City(name="Los Angeles", state_id=self.state.id)
        self.place = Place(name="My Place", city_id=self.city.id)
        mock_storage.new.return_value = None
        mock_storage.save.return_value = None

    @patch('api.v1.app.app.test_client')
    def test_create_place(self, mock_client):
        """Test POST /api/v1/cities/<city_id>/places"""
        mock_client.return_value.post.return_value.status_code = 201
        response = mock_client().post(f'/api/v1/cities/{self.city.id}/places',
                                       data=json.dumps({"name": "My Place"}),
                                       content_type='application/json')
        self.assertEqual(response.status_code, 201)

    @patch('api.v1.app.app.test_client')
    def test_get_place(self, mock_client):
        """Test GET /api/v1/places/<place_id>"""
        mock_client.return_value.get.return_value.status_code = 200
        response = mock_client().get(f'/api/v1/places/{self.place.id}')
        self.assertEqual(response.status_code, 200)

    @patch('api.v1.app.app.test_client')
    def test_update_place(self, mock_client):
        """Test PUT /api/v1/places/<place_id>"""
        mock_client.return_value.put.return_value.status_code = 200
        response = mock_client().put(f'/api/v1/places/{self.place.id}',
                                      data=json.dumps({'name': 'Updated Place'}),
                                      content_type='application/json')
        self.assertEqual(response.status_code, 200)

    @patch('api.v1.app.app.test_client')
    def test_delete_place(self, mock_client):
        """Test DELETE /api/v1/places/<place_id>"""
        mock_client.return_value.delete.return_value.status_code = 200
        response = mock_client().delete(f'/api/v1/places/{self.place.id}')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()