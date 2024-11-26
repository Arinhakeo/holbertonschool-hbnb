#!/usr/bin/python3
"""Tests for Review API endpoints"""
import unittest
import json
from api.v1.app import app
from models import storage
from models.user import User
from models.place import Place
from models.review import Review
from models.state import State
from models.city import City
import uuid

class TestReviewAPI(unittest.TestCase):
    """Test cases for Review API"""

def setUp(self):
    """Initialisation des données nécessaires pour les tests"""
    storage.rollback()  # Nettoyage de la session
    self.client = app.test_client()

    # IDs dynamiques
    self.state_id = str(uuid.uuid4())
    self.city_id = str(uuid.uuid4())
    self.user_id = str(uuid.uuid4())
    self.place_id = str(uuid.uuid4())
    self.review_id = str(uuid.uuid4())

    state = State(id=self.state_id, name="Test State")
    storage.new(state)
    storage.save()

    self.city = City(
        id=self.city_id,
        name="Test City",
        state_id=self.state_id
    )
    storage.new(self.city)
    storage.save()

    self.user = User(
        id=self.user_id,
        email="test@test.com",
        password="test123"
    )
    storage.new(self.user)
    storage.save()

    self.place = Place(
        id=self.place_id,
        city_id=self.city_id,
        user_id=self.user_id,
        name="Test Place",
        description="Test Description",
        number_rooms=2,
        number_bathrooms=1,
        max_guest=4,
        price_by_night=100
    )
    storage.new(self.place)
    storage.save()

    self.review = Review(
        id=self.review_id,
        place_id=self.place_id,
        user_id=self.user_id,
        text="Great place!"
    )
    storage.new(self.review)
    storage.save()

    # Headers pour les requêtes API
    self.headers = {'Content-Type': 'application/json'}

    def tearDown(self):
        """Nettoyer la base après chaque test"""
        storage.delete_all()
        storage.save()

    def test_get_reviews(self):
        """Test GET /api/v1/places/<place_id>/reviews"""
        response = self.client.get(f'/api/v1/places/{self.place.id}/reviews')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_get_review(self):
        """Test GET /api/v1/reviews/<review_id>"""
        response = self.client.get(f'/api/v1/reviews/{self.review.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['text'], 'Great place!')

    def test_create_review(self):
        """Test POST /api/v1/places/<place_id>/reviews"""
        data = {
            'user_id': self.user_id,
            'text': 'New review'
        }
        response = self.client.post(
            f'/api/v1/places/{self.place.id}/reviews',
            data=json.dumps(data),
            headers=self.headers
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['text'], 'New review')

    def test_update_review(self):
        """Test PUT /api/v1/reviews/<review_id>"""

        data = {'text': 'Updated review'}
        response = self.client.put(
            f'/api/v1/reviews/{self.review.id}',
            data=json.dumps(data),
            headers=self.headers
        )
        self.assertEqual(response.status_code, 200)

        # Vérifiez que le texte a été mis à jour
        self.assertEqual(response.json['text'], 'Updated review')

    def test_delete_review(self):
        """Test DELETE /api/v1/reviews/<review_id>"""
        response = self.client.delete(f'/api/v1/reviews/{self.review.id}')
        self.assertEqual(response.status_code, 200)

        # Vérifiez que la review est supprimée
        response = self.client.get(f'/api/v1/reviews/{self.review.id}')
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()