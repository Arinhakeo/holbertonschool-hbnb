import json
from functools import wraps
from models import storage
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review

def setup_test_db():
    """Setup test database with sample data"""
    storage.reload()
    
    # Create test user
    user = User(
        email="test@test.com",
        password="test123",
        first_name="Test",
        last_name="User"
    )
    user.save()
    
    # Create test state
    state = State(name="California")
    state.save()
    
    # Create test city
    city = City(
        state_id=state.id,
        name="San Francisco"
    )
    city.save()
    
    # Create test place
    place = Place(
        city_id=city.id,
        user_id=user.id,
        name="Test Place",
        description="Test Description",
        number_rooms=2,
        number_bathrooms=1,
        max_guest=4,
        price_by_night=100
    )
    place.save()
    
    # Create test amenity
    amenity = Amenity(name="WiFi")
    amenity.save()
    
    # Create test review
    review = Review(
        place_id=place.id,
        user_id=user.id,
        text="Great place!"
    )
    review.save()
    
    return {
        'user': user,
        'state': state,
        'city': city,
        'place': place,
        'amenity': amenity,
        'review': review
    }

def clear_test_db():
    """Clear all data from test database"""
    storage._DBStorage__session.query(Review).delete()
    storage._DBStorage__session.query(Place).delete()
    storage._DBStorage__session.query(City).delete()
    storage._DBStorage__session.query(State).delete()
    storage._DBStorage__session.query(User).delete()
    storage._DBStorage__session.query(Amenity).delete()
    storage._DBStorage__session.commit()

def with_test_db(f):
    """Decorator to setup and teardown test database"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        setup_test_db()
        try:
            return f(*args, **kwargs)
        finally:
            clear_test_db()
    return wrapper