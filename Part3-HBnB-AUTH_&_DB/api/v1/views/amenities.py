#!/usr/bin/python3
"""Routes for Amenity objects"""
from api.v1.views import app_views
from flask import jsonify, abort, request, current_app as app
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """Retrieve all amenities"""
    amenities = [amenity.to_dict() for amenity in storage.all(Amenity).values()]
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    """Retrieve an amenity by ID"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """Delete an amenity by ID"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    amenity.delete()
    storage.save()

    response = jsonify({})
    response.headers["Content-Type"] = "application/json"
    return response, 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """Create a new amenity"""
    try:
        amenity_data = request.get_json()
    except Exception:
        abort(400, "Not a JSON")
    if "name" not in amenity_data:
        abort(400, "Missing name")
    amenity = Amenity(**amenity_data)
    storage.new(amenity)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """Update an amenity by ID"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    try:
        amenity_data = request.get_json()
    except Exception:
        abort(400, "Not a JSON")
    for key, value in amenity_data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity, key, value)
    storage.save()
    return jsonify(amenity.to_dict())