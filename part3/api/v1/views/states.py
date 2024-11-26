#!/usr/bin/python3
"""States API views"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.state import State
from flasgger.utils import swag_from

@app_views.route('/states', methods=['GET'], strict_slashes=False)
@swag_from('documentation/states/get_states.yml')
def get_states():
    """Get all states"""
    states = [state.to_dict() for state in storage.all(State).values()]
    return jsonify(states)

@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/states/get_state.yml')
def get_state(state_id):
    """Retrieve a state by ID"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())

@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/states/delete_state.yml')
def delete_state(state_id):
    """Delete a state by ID"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    state.delete()
    storage.save()
    response = jsonify({})
    response.headers["Content-Type"] = "application/json"
    return response, 200

@app_views.route('/states', methods=['POST'], strict_slashes=False)
@swag_from('documentation/states/post_state.yml')
def create_state():
    """Create a new state"""
    try:
        state_data = request.get_json()
    except Exception:
        abort(400, "Not a JSON")
    if "name" not in state_data:
        abort(400, "Missing name")
    existing_state = storage.get_by_name(State, state_data["name"])
    if existing_state:
        return jsonify(existing_state.to_dict()), 200
    state = State(**state_data)
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), 201

@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/states/put_state.yml')
def update_state(state_id):
    """Update state"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    data = request.get_json()
    ignore = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict())