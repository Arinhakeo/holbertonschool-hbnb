import unittest
from models.engine.db_storage import DBStorage
from models.base_model import Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
import os

class TestDBStorage(unittest.TestCase):
    """Test cases for DBStorage"""

    @classmethod
    def setUpClass(cls):
        """Set up the test database and initialize DBStorage"""
        cls.storage = DBStorage()
        cls.storage.reload()  # Ensure session is initialized
        cls.test_objects = []

    @classmethod
    def tearDownClass(cls):
        """Clean up after all tests"""
        for obj in cls.test_objects:
            cls.storage.delete(obj)
        cls.storage.save()

    def setUp(self):
        """Set up data for each test"""
        self.user = User(email="test@test.com", password="test123")
        self.state = State(name="California")
        self.city = City(name="San Francisco", state_id=self.state.id)
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
        self.amenity = Amenity(name="WiFi")
        self.review = Review(
            place_id=self.place.id,
            user_id=self.user.id,
            text="Great place!"
        )
        # Add objects to test_objects for cleanup
        self.test_objects = [self.user, self.state, self.city, self.place, self.amenity, self.review]

    def test_all(self):
        """Test retrieving all objects"""
        self.storage.new(self.user)
        self.storage.new(self.state)
        self.storage.save()

        all_objs = self.storage.all()
        self.assertIsInstance(all_objs, dict)
        self.assertIn(f"User.{self.user.id}", all_objs)
        self.assertIn(f"State.{self.state.id}", all_objs)

        state_objs = self.storage.all(State)
        self.assertIsInstance(state_objs, dict)
        self.assertIn(f"State.{self.state.id}", state_objs)

    def test_new(self):
        """Test adding a new object"""
        self.storage.new(self.user)
        self.storage.save()
        result = self.storage.all(User)
        self.assertIn(f"User.{self.user.id}", result)

    def test_save(self):
        """Test saving objects"""
        self.storage.new(self.state)
        self.storage.save()
        result = self.storage.all(State)
        self.assertIn(f"State.{self.state.id}", result)

    def test_delete(self):
        """Test deleting an object"""
        self.storage.new(self.city)
        self.storage.save()
        self.storage.delete(self.city)
        self.storage.save()
        result = self.storage.all(City)
        self.assertNotIn(f"City.{self.city.id}", result)

    def test_reload(self):
        """Test reloading objects from the database"""
        self.storage.new(self.place)
        self.storage.save()
        self.storage.reload()
        result = self.storage.all(Place)
        self.assertIn(f"Place.{self.place.id}", result)

if __name__ == '__main__':
    unittest.main()
