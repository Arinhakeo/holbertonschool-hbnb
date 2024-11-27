#!/usr/bin/python3
"""Routes for User objects"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.user import User

@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """Retrieve all users"""
    users = [user.to_dict() for user in storage.all(User).values()]
    return jsonify(users)

@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Retrieve a user by ID"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())

@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Create a new user"""
    try:
        user_data = request.get_json()
    except Exception:
        abort(400, "Not a JSON")
    if "email" not in user_data:
        abort(400, "Missing email")
    if "password" not in user_data:
        abort(400, "Missing password")
    user = User(**user_data)
    storage.new(user)
    storage.save()
    return jsonify(user.to_dict()), 201

@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Update a user by ID"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    try:
        user_data = request.get_json()
    except Exception:
        abort(400, "Not a JSON")
    for key, value in user_data.items():
        if key not in ["id", "email", "created_at", "updated_at"]:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict())

@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Delete a user by ID"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    user.delete()
    storage.save()
    response = jsonify({})
    response.headers["Content-Type"] = "application/json"
    return response, 200