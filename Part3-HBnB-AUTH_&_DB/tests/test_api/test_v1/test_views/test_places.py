#!/usr/bin/python3
"""Tests for Place API endpoints"""
import unittest
import json
from api.v1.app import app
from models import storage
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
import uuid


class TestPlaceAPI(unittest.TestCase):
    """Test cases for Place API"""

    def setUp(self):
        storage.rollback()
        """Initialisation des données nécessaires pour les tests"""
        self.client = app.test_client()

        # Headers pour les requêtes JSON
        self.headers = {"Content-Type": "application/json"}

        # Générer des IDs dynamiques
        self.state_id = str(uuid.uuid4())
        self.city_id = str(uuid.uuid4())
        self.user_id = str(uuid.uuid4())
        self.place_id = str(uuid.uuid4())

        # Ajouter un état
        state = State(id=self.state_id, name="Test State")
        storage.new(state)

        # Ajouter une ville associée
        city = City(id=self.city_id, name="Test City", state_id=self.state_id)
        storage.new(city)
        self.city = city  # Stocker pour les tests

        # Ajouter un utilisateur
        user = User(id=self.user_id, email="user@example.com", password="password")
        storage.new(user)
        self.user = user  # Stocker pour les tests

        # Ajouter un lieu associé
        place = Place(
            id=self.place_id,
            name="Test Place",
            user_id=self.user_id,
            city_id=self.city_id,
            number_rooms=3,
            number_bathrooms=2,
            max_guest=4,
            price_by_night=100.0
        )
        storage.new(place)
        self.place = place  # Stocker pour les tests

        storage.save()

    def tearDown(self):
        """Nettoyer la base après chaque test"""
        storage.delete_all()
        storage.save()

    def test_get_places(self):
        """Test GET /api/v1/cities/<city_id>/places"""
        response = self.client.get(f'/api/v1/cities/{self.city_id}/places')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_get_place(self):
        """Test GET /api/v1/places/<place_id>"""
        response = self.client.get(f'/api/v1/places/{self.place_id}')
        self.assertEqual(response.status_code, 200)

        # Vérifiez le contenu JSON
        data = response.json
        self.assertEqual(data['id'], self.place_id)
        self.assertEqual(data['name'], 'Test Place')

    def test_create_place(self):
        """Test POST /api/v1/cities/<city_id>/places"""
        data = {
            'user_id': self.user_id,
            'name': 'New Place',
            'description': 'New Description',
            'number_rooms': 2,
            'number_bathrooms': 2,
            'max_guest': 4,
            'price_by_night': 200
        }
        response = self.client.post(
            f'/api/v1/cities/{self.city_id}/places',
            data=json.dumps(data),
            headers=self.headers
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], 'New Place')

    def test_update_place(self):
        """Test PUT /api/v1/places/<place_id>"""
        data = {'name': 'Updated Place'}
        response = self.client.put(
            f'/api/v1/places/{self.place_id}',
            data=json.dumps(data),
            headers=self.headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'Updated Place')

    def test_delete_place(self):
        """Test DELETE /api/v1/places/<place_id>"""
        response = self.client.delete(f'/api/v1/places/{self.place_id}')
        self.assertEqual(response.status_code, 200)

        # Vérifiez que le lieu a été supprimé
        response = self.client.get(f'/api/v1/places/{self.place_id}')
        self.assertEqual(response.status_code, 404)

    def test_places_search(self):
        """Test POST /api/v1/places_search"""
        data = {
            "states": [self.state_id],
            "cities": [self.city_id],
            "amenities": []
        }
        response = self.client.post(
            '/api/v1/places_search',
            data=json.dumps(data),
            headers=self.headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)