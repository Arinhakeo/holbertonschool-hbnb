#!/usr/bin/python3
"""Test Place-Amenity API endpoints"""
import unittest
import json
from api.v1.app import app
from models import storage
from models.place import Place
from models.amenity import Amenity
from models.state import State
from models.city import City
from models.user import User
import uuid

class TestPlaceAmenitiesAPI(unittest.TestCase):
    """Test cases for Place-Amenity API"""

    def setUp(self):
        """Set up test environment"""
        try:
            storage.rollback()
            self.client = app.test_client()
            self.headers = {'Content-Type': 'application/json'}

            # Create test data
            self.state = State(name="Test State")
            storage.new(self.state)
            storage.save()

            self.city = City(name="Test City", state_id=self.state.id)
            storage.new(self.city)
            storage.save()

            self.user = User(
                email="test@test.com",
                password="test123",
                first_name="Test",
                last_name="User"
            )
            storage.new(self.user)
            storage.save()

            self.place = Place(
                city_id=self.city.id,
                user_id=self.user.id,
                name="Test Place",
                description="Test Description",
                number_rooms=2,
                number_bathrooms=1,
                max_guest=4,
                price_by_night=100
            )
            storage.new(self.place)
            storage.save()

            self.amenity = Amenity(name="Test Amenity")
            storage.new(self.amenity)
            storage.save()

        except Exception as e:
            print(f"Error in setUp: {str(e)}")
            storage.rollback()
            raise

    def tearDown(self):
        """Clean up test environment"""
        storage.rollback()
        storage.delete_all()
        storage.save()

    def test_link_amenity_to_place(self):
        """Test POST /api/v1/places/<place_id>/amenities/<amenity_id>"""
        response = self.client.post(
            f'/api/v1/places/{self.place.id}/amenities/{self.amenity.id}'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['id'], self.amenity.id)

    def test_unlink_amenity_from_place(self):
        """Test DELETE /api/v1/places/<place_id>/amenities/<amenity_id>"""
        # First link the amenity
        self.client.post(
            f'/api/v1/places/{self.place.id}/amenities/{self.amenity.id}'
        )
        
        # Then try to unlink it
        response = self.client.delete(
            f'/api/v1/places/{self.place.id}/amenities/{self.amenity.id}'
        )
        self.assertEqual(response.status_code, 200)

    def test_get_place_amenities(self):
        """Test GET /api/v1/places/<place_id>/amenities"""
        response = self.client.get(
            f'/api/v1/places/{self.place.id}/amenities'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)