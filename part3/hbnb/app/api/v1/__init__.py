"""API v1 initialization."""

from app.api.v1.admin import api as admin_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.users import api as users_ns
from app.api.v1.auth import api as auth_ns
from flask_restx import Api

api = Api(version="1.0", title="HBnB API", description="HolbertonBnB REST API")


api.add_namespace(auth_ns, path="/api/v1/auth")
api.add_namespace(users_ns, path="/api/v1/users")
api.add_namespace(places_ns, path="/api/v1/places")
api.add_namespace(amenities_ns, path="/api/v1/amenities")
api.add_namespace(reviews_ns, path="/api/v1/reviews")
api.add_namespace(admin_ns, path="/api/v1/admin")