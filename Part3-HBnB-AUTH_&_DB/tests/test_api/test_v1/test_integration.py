#!/usr/bin/python3
"""Test integration module"""
import unittest
import json
from api.v1.app import app
from models import storage
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review

class TestIntegration(unittest.TestCase):
    def setUp(self):
        """Set up test environment"""
        print("\n=== Setting up test environment ===")
        self.client = app.test_client()
        self.headers = {'Content-Type': 'application/json'}
        storage.rollback()
        storage.delete_all()
        storage.save()
        print("Environment setup complete")

    def tearDown(self):
        """Clean up test environment"""
        print("\n=== Cleaning up test environment ===")
        storage.delete_all()
        storage.save()
        print("Cleanup complete")

    def verify_object_exists(self, obj_type, obj_id):
        """Helper to verify object exists in database"""
        print(f"\nVerifying {obj_type.__name__} with id {obj_id}")
        obj = storage.get(obj_type, obj_id)
        if obj:
            print(f"Found {obj_type.__name__}: {obj.to_dict()}")
        else:
            print(f"WARNING: {obj_type.__name__} not found!")
        self.assertIsNotNone(obj, f"{obj_type.__name__} with id {obj_id} not found in database")
        return obj

    def test_full_booking_flow(self):
        """Test complete booking flow"""
        try:
            print("\n=== Starting full booking flow test ===")

            # 1. Create user
            print("\n--- Creating user ---")
            user_data = {
                'email': 'test@test.com',
                'password': 'test123',
                'first_name': 'Test',
                'last_name': 'User'
            }
            print(f"User data to send: {user_data}")
            response = self.client.post(
                '/api/v1/users',
                data=json.dumps(user_data),
                headers=self.headers
            )
            print(f"User creation response: {response.data}")
            self.assertEqual(response.status_code, 201)
            user_id = response.json['id']
            user = self.verify_object_exists(User, user_id)

            # 2. Create state
            print("\n--- Creating state ---")
            state_data = {'name': 'California'}
            print(f"State data to send: {state_data}")
            response = self.client.post(
                '/api/v1/states',
                data=json.dumps(state_data),
                headers=self.headers
            )
            print(f"State creation response: {response.data}")
            self.assertEqual(response.status_code, 201)
            state_id = response.json['id']
            state = self.verify_object_exists(State, state_id)

            # 3. Create city
            print("\n--- Creating city ---")
            city_data = {
                'name': 'San Francisco',
                'state_id': state_id
            }
            print(f"City data to send: {city_data}")
            response = self.client.post(
                f'/api/v1/states/{state_id}/cities',
                data=json.dumps(city_data),
                headers=self.headers
            )
            print(f"City creation response: {response.data}")
            self.assertEqual(response.status_code, 201)
            city_id = response.json['id']
            city = self.verify_object_exists(City, city_id)

            # 4. Create place
            print("\n--- Creating place ---")
            place_data = {
                'name': 'Cozy Apartment',
                'user_id': user_id,
                'city_id': city_id,
                'description': 'A lovely place in the heart of the city',
                'number_rooms': 2,
                'number_bathrooms': 1,
                'max_guest': 4,
                'price_by_night': 100
            }
            print(f"Place data to send: {place_data}")
            response = self.client.post(
                f'/api/v1/cities/{city_id}/places',
                data=json.dumps(place_data),
                headers=self.headers
            )
            print(f"Place creation response: {response.data}")
            self.assertEqual(response.status_code, 201)
            place_id = response.json['id']
            place = self.verify_object_exists(Place, place_id)

            # 5. Create and link amenity
            print("\n--- Creating amenity ---")
            amenity_data = {'name': 'WiFi'}
            print(f"Amenity data to send: {amenity_data}")
            response = self.client.post(
                '/api/v1/amenities',
                data=json.dumps(amenity_data),
                headers=self.headers
            )
            print(f"Amenity creation response: {response.data}")
            self.assertEqual(response.status_code, 201)
            amenity_id = response.json['id']
            amenity = self.verify_object_exists(Amenity, amenity_id)

            # Link amenity to place
            print("\n--- Linking amenity to place ---")
            response = self.client.post(
                f'/api/v1/places/{place_id}/amenities/{amenity_id}',
                headers=self.headers
            )
            print(f"Amenity linking response: {response.data}")
            self.assertEqual(response.status_code, 200)

            # Verify the link
            print("\n--- Verifying amenity-place link ---")
            response = self.client.get(
                f'/api/v1/places/{place_id}/amenities',
                headers=self.headers
            )
            print(f"Place amenities: {response.data}")

            # 6. Create review
            print("\n--- Creating review ---")
            review_data = {
                'user_id': user_id,
                'text': 'Amazing place!'
            }
            print(f"Review data to send: {review_data}")
            response = self.client.post(
                f'/api/v1/places/{place_id}/reviews',
                data=json.dumps(review_data),
                headers=self.headers
            )
            print(f"Review creation response: {response.data}")
            self.assertEqual(response.status_code, 201)
            review_id = response.json['id']
            review = self.verify_object_exists(Review, review_id)

            # 7. Verify everything with a search
            print("\n--- Testing search functionality ---")
            search_data = {
                'states': [state_id],
                'cities': [city_id],
                'amenities': [amenity_id]
            }
            print(f"Search data to send: {search_data}")
            
            # Verify objects exist before search
            print("\nVerifying objects before search:")
            print(f"State exists: {storage.get(State, state_id) is not None}")
            print(f"City exists: {storage.get(City, city_id) is not None}")
            print(f"Amenity exists: {storage.get(Amenity, amenity_id) is not None}")
            
            response = self.client.post(
                '/api/v1/places_search',
                data=json.dumps(search_data),
                headers=self.headers
            )
            print(f"Search response status: {response.status_code}")
            print(f"Search response data: {response.data.decode()}")
            
            self.assertEqual(response.status_code, 200)
            self.assertTrue(len(response.json) > 0)
            print("\n=== Full booking flow test completed successfully ===")

        except Exception as e:
            print(f"\n!!! Test failed with error: {str(e)}")
            import traceback
            print(f"Traceback:\n{traceback.format_exc()}")
            storage.rollback()
            raise

if __name__ == '__main__':
    unittest.main()