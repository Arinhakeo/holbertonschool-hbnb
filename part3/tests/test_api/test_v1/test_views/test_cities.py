#!/usr/bin/python3
"""Tests for City API endpoints"""
import unittest
import json
from api.v1.app import app
from models import storage
from models.state import State
from models.city import City
import uuid


class TestCityAPI(unittest.TestCase):
    """Test cases for City API"""

    def setUp(self):
        storage.rollback()
        """Initialisation des données nécessaires pour les tests"""
        self.client = app.test_client()

        # Générer des IDs dynamiques
        self.state_id = str(uuid.uuid4())  # ID pour l'état
        self.city_id = str(uuid.uuid4())  # ID pour la ville

        # Ajouter un état
        self.state = State(id=self.state_id, name="Test State")
        storage.new(self.state)

        # Ajouter une ville associée
        self.city = City(id=self.city_id, name="Test City", state_id=self.state_id)
        storage.new(self.city)

        # Sauvegarder les données dans le stockage
        storage.save()

    def tearDown(self):
        """Nettoyer la base après chaque test"""
        storage.delete_all()
        storage.save()

    def test_get_cities(self):
        """Test GET /api/v1/states/<state_id>/cities"""
        response = self.client.get(f'/api/v1/states/{self.state_id}/cities')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        self.assertGreaterEqual(len(response.json), 1)  # Au moins 1 ville existe

    def test_get_city(self):
        """Test GET /api/v1/cities/<city_id>"""
        response = self.client.get(f'/api/v1/cities/{self.city_id}')
        self.assertEqual(response.status_code, 200)

        # Vérifiez les informations retournées
        data = response.json
        self.assertEqual(data['id'], self.city_id)
        self.assertEqual(data['name'], 'Test City')

    def test_create_city(self):
        """Test POST /api/v1/states/<state_id>/cities"""
        data = {'name': 'Los Angeles'}
        response = self.client.post(
            f'/api/v1/states/{self.state_id}/cities',
            data=json.dumps(data),
            headers={"Content-Type": "application/json"}
        )
        self.assertEqual(response.status_code, 201)

        # Vérifiez les informations retournées
        data = response.json
        self.assertEqual(data['name'], 'Los Angeles')

    def test_update_city(self):
        """Test PUT /api/v1/cities/<city_id>"""
        data = {'name': 'Updated City'}
        response = self.client.put(
            f'/api/v1/cities/{self.city_id}',
            data=json.dumps(data),
            headers={"Content-Type": "application/json"}
        )
        self.assertEqual(response.status_code, 200)

        # Vérifiez que le nom de la ville a été mis à jour
        data = response.json
        self.assertEqual(data['name'], 'Updated City')

    def test_delete_city(self):
        """Test DELETE /api/v1/cities/<city_id>"""
        response = self.client.delete(f'/api/v1/cities/{self.city_id}')
        self.assertEqual(response.status_code, 200)

        # Vérifiez que la ville est supprimée
        response = self.client.get(f'/api/v1/cities/{self.city_id}')
        self.assertEqual(response.status_code, 404)