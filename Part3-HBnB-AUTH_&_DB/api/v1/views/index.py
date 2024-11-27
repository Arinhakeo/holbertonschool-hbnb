#!/usr/bin/python3
"""Index view"""
from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Status of API"""
    return jsonify({"status": "OK"})

@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """Get stats of objects"""
    from models import storage
    stats = {}
    stats['amenities'] = storage.count("Amenity")
    stats['cities'] = storage.count("City")
    stats['places'] = storage.count("Place")
    stats['reviews'] = storage.count("Review")
    stats['states'] = storage.count("State")
    stats['users'] = storage.count("User")
    return jsonify(stats)