from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User

@app_views.route('/places/<place_id>/reviews', methods=['GET'], strict_slashes=False)
def get_place_reviews(place_id):
    """Retrieve all reviews for a given place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)

@app_views.route('/places/<place_id>/reviews', methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """Create a new review"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    try:
        review_data = request.get_json()
    except Exception:
        abort(400, description="Not a JSON")

    if "user_id" not in review_data:
        abort(400, description="Missing user_id")

    user = storage.get(User, review_data['user_id'])
    if not user:
        abort(404)

    if "text" not in review_data:
        abort(400, description="Missing text")

    review_data['place_id'] = place_id

    try:
        review = Review(**review_data)
        storage.new(review)
        storage.save()
        return jsonify(review.to_dict()), 201
    except Exception as e:
        storage.rollback()
        print(f"Error creating review: {str(e)}")
        abort(500)

@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Retrieve a specific review"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())

@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """Update a review"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    
    try:
        data = request.get_json()
    except Exception:
        abort(400, "Not a JSON")
        
    ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(review, key, value)
            
    storage.save()
    return jsonify(review.to_dict())

@app_views.route('/reviews/<review_id>', methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """Delete a review"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
        
    storage.delete(review)
    storage.save()
    return jsonify({}), 200