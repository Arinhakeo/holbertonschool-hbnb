"""API v1 endpoints - Main configuration file for the API"""
from flask import Blueprint
from flask_restx import Api
from app.api.v1.users import api as user_ns
from app.api.v1.places import api as place_ns  
from app.api.v1.reviews import api as review_ns
from app.api.v1.amenities import api as amenity_ns

# Create Blueprint for API v1
blueprint = Blueprint('api_v1', __name__, url_prefix='/api/v1')

# Initialize API with Swagger documentation
api = Api(
    blueprint,
    title='HBnB REST API', 
    version='1.0',
    description='API for managing users, places, reviews and amenities'
)

# Register all namespaces/routes
api.add_namespace(user_ns)
api.add_namespace(place_ns)
api.add_namespace(review_ns)
api.add_namespace(amenity_ns)

# Important: Make blueprint available for import
__all__ = ['blueprint']