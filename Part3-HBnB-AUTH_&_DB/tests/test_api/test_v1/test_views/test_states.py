#!/usr/bin/python3
"""Tests for State API endpoints"""
import unittest
import json
from api.v1.app import app
from models import storage
from models.state import State
import uuid


class TestStateAPI(unittest.TestCase):
    """Test cases for State API"""

    def setUp(self):
        storage.rollback()
        """Initialisation des données nécessaires pour les tests"""
        self.client = app.test_client()

        # Headers pour les requêtes JSON
        self.headers = {"Content-Type": "application/json"}

        # Générer un ID dynamique pour l'état
        self.state_id = str(uuid.uuid4())

        # Ajouter un état dans la base
        self.state = State(id=self.state_id, name="Test State")
        storage.new(self.state)
        storage.save()

    def tearDown(self):
        """Nettoyer la base après chaque test"""
        storage.delete_all()  # Suppression des données
        storage.save()

    def test_get_states(self):
        """Test GET /api/v1/states/"""
        response = self.client.get('/api/v1/states')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        self.assertGreaterEqual(len(response.json), 1)  # Vérifie qu'au moins 1 état existe

    def test_get_state(self):
        """Test GET /api/v1/states/<state_id>"""
        response = self.client.get(f'/api/v1/states/{self.state_id}')
        self.assertEqual(response.status_code, 200)

        # Vérifiez les informations retournées
        data = response.json
        self.assertEqual(data['id'], self.state_id)
        self.assertEqual(data['name'], 'Test State')

    def test_create_state(self):
        """Test POST /api/v1/states/"""
        data = {'name': 'New York'}
        response = self.client.post(
            '/api/v1/states',
            data=json.dumps(data),
            headers=self.headers
        )
        self.assertEqual(response.status_code, 201)

        # Vérifiez les informations retournées
        data = response.json
        self.assertEqual(data['name'], 'New York')

    def test_update_state(self):
        """Test PUT /api/v1/states/<state_id>"""
        data = {'name': 'Updated State'}
        response = self.client.put(
            f'/api/v1/states/{self.state_id}',
            data=json.dumps(data),
            headers=self.headers
        )
        self.assertEqual(response.status_code, 200)

        # Vérifiez que le nom de l'état a été mis à jour
        data = response.json
        self.assertEqual(data['name'], 'Updated State')

    def test_delete_state(self):
        """Test DELETE /api/v1/states/<state_id>"""
        response = self.client.delete(f'/api/v1/states/{self.state_id}')
        self.assertEqual(response.status_code, 200)

        # Vérifiez que l'état a été supprimé
        response = self.client.get(f'/api/v1/states/{self.state_id}')
        self.assertEqual(response.status_code, 404)