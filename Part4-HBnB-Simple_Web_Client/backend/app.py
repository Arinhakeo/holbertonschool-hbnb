#!/usr/bin/python3
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from models import storage
from models.place import Place
from models.user import User
from models.city import City
import os

# Chemins relatifs corrects puisque app.py est dans le dossier backend
app = Flask(__name__,)
CORS(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/places', methods=['GET'])
def get_places():
    places = storage.all(Place).values()
    return jsonify([place.to_dict() for place in places])


@app.route('/api/places/<place_id>', methods=['GET'])
def get_place(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        return jsonify({'error': 'Place not found'}), 404
    return jsonify(place.to_dict())


@app.route('/api/places', methods=['POST'])
def create_place():
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400

    data = request.get_json()
    required_fields = ['name', 'city_id', 'user_id', 'description', 'number_rooms',
                       'number_bathrooms', 'max_guest', 'price_by_night']

    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing {field}'}), 400

    place = Place(**data)
    storage.new(place)
    storage.save()
    return jsonify(place.to_dict()), 201


@app.route('/api/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        return jsonify({'error': 'Place not found'}), 404

    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400

    data = request.get_json()
    ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']

    for key, value in data.items():
        if key not in ignore_keys:
            setattr(place, key, value)

    storage.save()
    return jsonify(place.to_dict())


@app.route('/api/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        return jsonify({'error': 'Place not found'}), 404

    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app.teardown_appcontext
def teardown_db(exception):
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
