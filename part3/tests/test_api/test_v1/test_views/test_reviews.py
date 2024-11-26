#!/usr/bin/python3
"""Tests for Review API endpoints"""
import unittest
import json
from api.v1.app import app
from models import storage
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.review import Review
import uuid

class TestReviewAPI(unittest.TestCase):
    """Test cases for Review API"""

    def setUp(self):
        """Initialisation des données nécessaires pour les tests"""
        try:
            storage.rollback()
            storage.delete_all()  # Nettoie la base avant de commencer
            
            self.client = app.test_client()
            self.headers = {'Content-Type': 'application/json'}

            # Création des IDs
            self.state_id = str(uuid.uuid4())
            self.city_id = str(uuid.uuid4())
            self.user_id = str(uuid.uuid4())
            self.place_id = str(uuid.uuid4())
            self.review_id = str(uuid.uuid4())

            # État
            self.state = State(id=self.state_id, name="Test State")
            storage.new(self.state)
            storage.save()

            # Ville
            self.city = City(
                id=self.city_id,
                name="Test City",
                state_id=self.state_id
            )
            storage.new(self.city)
            storage.save()

            # Utilisateur
            self.user = User(
                id=self.user_id,
                email="test@test.com",
                password="test123"
            )
            storage.new(self.user)
            storage.save()

            # Place
            self.place = Place(
                id=self.place_id,
                name="Test Place",
                city_id=self.city_id,
                user_id=self.user_id,
                description="Test Description",
                number_rooms=2,
                number_bathrooms=1,
                max_guest=4,
                price_by_night=100
            )
            storage.new(self.place)
            storage.save()

            # Review
            self.review = Review(
                id=self.review_id,
                place_id=self.place_id,
                user_id=self.user_id,
                text="Great place!"
            )
            storage.new(self.review)
            storage.save()

            created_review = storage.get(Review, self.review_id)
            if not created_review:
                raise Exception(f"Review {self.review_id} not found after creation")

            # Vérification de la place
            created_place = storage.get(Place, self.place_id)
            if not created_place:
                raise Exception(f"Place {self.place_id} not found")

            print(f"Review created: {created_review.id}")
            print(f"Place found: {created_place.id}")


        except Exception as e:
            print(f"Error in setUp: {str(e)}")
            storage.rollback()
            raise

    def tearDown(self):
        """Nettoyer après chaque test"""
        try:
            storage.delete_all()
            storage.save()
        except Exception as e:
            print(f"Error in tearDown: {str(e)}")
            storage.rollback()

    def test_get_reviews(self):
        """Test GET /api/v1/places/<place_id>/reviews"""
        response = self.client.get(f'/api/v1/places/{self.place_id}/reviews')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_get_review(self):
        """Test GET /api/v1/reviews/<review_id>"""
        response = self.client.get(f'/api/v1/reviews/{self.review_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['text'], 'Great place!')

    def test_create_review(self):
        """Test POST /api/v1/places/<place_id>/reviews"""
        new_review_data = {
            'user_id': self.user_id,
            'text': 'Another great review!'
        }
        response = self.client.post(
            f'/api/v1/places/{self.place_id}/reviews',
            data=json.dumps(new_review_data),
            headers=self.headers
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['text'], 'Another great review!')

    def test_update_review(self):
        """Test PUT /api/v1/reviews/<review_id>"""
        update_data = {'text': 'Updated review text'}
        response = self.client.put(
            f'/api/v1/reviews/{self.review_id}',
            data=json.dumps(update_data),
            headers=self.headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['text'], 'Updated review text')

    def test_delete_review(self):
        """Test DELETE /api/v1/reviews/<review_id>"""
        response = self.client.delete(f'/api/v1/reviews/{self.review_id}')
        self.assertEqual(response.status_code, 200)