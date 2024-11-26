#!/usr/bin/python3
"""Tests for Amenity API endpoints"""
import unittest
import json
from api.v1.app import app
from models import storage
from models.amenity import Amenity
import uuid


class TestAmenityAPI(unittest.TestCase):
    """Test cases for Amenity API"""

    def setUp(self):
        storage.rollback()
        """Initialisation des données nécessaires pour les tests"""
        self.client = app.test_client()

        # Headers pour les requêtes JSON
        self.headers = {"Content-Type": "application/json"}

        # Générer un ID dynamique pour l'amenity
        self.amenity_id = str(uuid.uuid4())

        # Ajouter une amenity
        self.amenity = Amenity(id=self.amenity_id, name="Test Amenity")
        storage.new(self.amenity)
        storage.save()

    def tearDown(self):
        """Nettoyer la base après chaque test"""
        storage.delete_all()
        storage.save()

    def test_get_amenities(self):
        """Test GET /api/v1/amenities"""
        response = self.client.get('/api/v1/amenities')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_create_amenity(self):
        """Test POST /api/v1/amenities"""
        data = {'name': 'WiFi'}
        response = self.client.post(
            '/api/v1/amenities',
            data=json.dumps(data),
            headers=self.headers
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], 'WiFi')

    def test_get_amenity(self):
        """Test GET /api/v1/amenities/<amenity_id>"""
        response = self.client.get(f'/api/v1/amenities/{self.amenity.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'Test Amenity')

    def test_update_amenity(self):
        """Test PUT /api/v1/amenities/<amenity_id>"""
        data = {'name': 'Updated WiFi'}
        response = self.client.put(
            f'/api/v1/amenities/{self.amenity.id}',
            data=json.dumps(data),
            headers=self.headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'Updated WiFi')

    def test_delete_amenity(self):
        """Test DELETE /api/v1/amenities/<amenity_id>"""
        response = self.client.delete(f'/api/v1/amenities/{self.amenity_id}')
        self.assertEqual(response.status_code, 200)

        # Vérifiez que l'amenity est supprimée
        response = self.client.get(f'/api/v1/amenities/{self.amenity_id}')
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()