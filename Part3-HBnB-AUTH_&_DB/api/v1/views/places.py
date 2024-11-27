#!/usr/bin/python3
"""Places API views"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.city import City
from models.user import User
from models.place import Place
from models.state import State
from models.amenity import Amenity

@app_views.route('/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def get_places(city_id):
    """Get all places of a city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify([place.to_dict() for place in city.places])

@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Get place by id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())

@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Delete a place by ID"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    place.delete()
    storage.save()

    response = jsonify({})
    response.headers["Content-Type"] = "application/json"
    return response, 200

@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """Create a new Place for a given City"""

    # Vérifiez que la City existe
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    # Parsez les données JSON
    try:
        place_data = request.get_json()
    except Exception:
        abort(400, "Not a JSON")

    # Vérifiez que 'user_id' est fourni
    if "user_id" not in place_data:
        abort(400, "Missing user_id")

    # Vérifiez que l'utilisateur existe
    user = storage.get(User, place_data["user_id"])
    if not user:
        abort(404)

    # Vérifiez que 'name' est fourni
    if "name" not in place_data:
        abort(400, "Missing name")

    # Injectez le city_id
    place_data["city_id"] = city_id

    # Créez le Place
    place = Place(**place_data)
    storage.new(place)
    storage.save()
    return jsonify(place.to_dict()), 201

@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Update place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    data = request.get_json()
    ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict())

@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """Search places based on states, cities and amenities"""
    try:
        print("\n=== Starting places_search ===")
        if not request.get_json():
            print("No JSON data received")
            abort(400, description="Not a JSON")
        
        data = request.get_json()
        print(f"\nReceived search data: {data}")
        places = []

        # Si aucun critère n'est fourni
        if not data or (not data.get('states') and 
                       not data.get('cities') and 
                       not data.get('amenities')):
            print("\nNo search criteria - returning all places")
            all_places = storage.all(Place).values()
            return jsonify([place.to_dict() for place in all_places])

        # Chercher par states
        if data.get('states'):
            print(f"\nSearching by states: {data['states']}")
            for state_id in data['states']:
                state = storage.get(State, state_id)
                print(f"Found state: {state.name if state else 'None'}")
                if state:
                    for city in state.cities:
                        print(f"Processing city: {city.name}")
                        places.extend([place for place in city.places])
                        print(f"Places found in {city.name}: {len(city.places)}")

        # Chercher par cities
        if data.get('cities'):
            print(f"\nSearching by cities: {data['cities']}")
            cities_places = []
            for city_id in data['cities']:
                city = storage.get(City, city_id)
                print(f"Found city: {city.name if city else 'None'}")
                if city:
                    city_places = [place for place in city.places]
                    print(f"Places found in {city.name}: {len(city_places)}")
                    cities_places.extend(city_places)

            if places:
                print("Filtering existing places by cities")
                places = [p for p in places if p in cities_places]
            else:
                places = cities_places
            print(f"Total places after city filtering: {len(places)}")

        # Filtrer par amenities
        if data.get('amenities'):
            print(f"\nFiltering by amenities: {data['amenities']}")
            amenities = []
            for amenity_id in data['amenities']:
                amenity = storage.get(Amenity, amenity_id)
                print(f"Found amenity: {amenity.name if amenity else 'None'}")
                if amenity:
                    amenities.append(amenity)

            # Si on n'a pas encore de places, prendre toutes les places
            if not places:
                print("No places yet, getting all places")
                places = list(storage.all(Place).values())

            # Vérifier les amenities pour chaque place
            filtered_places = []
            for place in places:
                print(f"\nChecking amenities for place: {place.id}")
                place_amenities = [a for a in place.amenities]
                print(f"Place amenities: {[a.name for a in place_amenities]}")
                if all(am in place_amenities for am in amenities):
                    filtered_places.append(place)
            places = filtered_places
            print(f"Places after amenity filtering: {len(places)}")

        # Convertir en dictionnaires
        print("\nConverting places to dictionaries")
        place_dicts = []
        for place in places:
            try:
                place_dict = place.to_dict()
                place_dicts.append(place_dict)
                print(f"Successfully converted place {place.id}")
            except Exception as e:
                print(f"Error converting place {place.id}: {str(e)}")

        print(f"\nFinal number of places: {len(place_dicts)}")
        return jsonify(place_dicts)

    except Exception as e:
        print(f"\n=== Error in places_search ===")
        print(f"Type: {type(e)}")
        print(f"Message: {str(e)}")
        import traceback
        print(f"Traceback:\n{traceback.format_exc()}")
        abort(500, description=str(e))
        
@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_place_amenities(place_id):
    """Get all amenities of a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify([amenity.to_dict() for amenity in place.amenities])

@app_views.route('/places/<place_id>/amenities/<amenity_id>', 
                methods=['POST'], strict_slashes=False)
def link_amenity_to_place(place_id, amenity_id):
    """Link an amenity to a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    if amenity in place.amenities:
        return jsonify(amenity.to_dict())

    place.amenities.append(amenity)
    storage.save()
    return jsonify(amenity.to_dict())

@app_views.route('/places/<place_id>/amenities/<amenity_id>', 
                methods=['DELETE'], strict_slashes=False)
def unlink_amenity_from_place(place_id, amenity_id):
    """Unlink an amenity from a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    if amenity not in place.amenities:
        abort(404)

    place.amenities.remove(amenity)
    storage.save()
    return jsonify({}), 200