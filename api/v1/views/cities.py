#!/usr/bin/python3
"""
Index route for AirBnB clone v3 API v1
"""


from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State
from flask import jsonify, request, abort


@app_views.route("/states/<state_id>/cities",
                 strict_slashes=False,
                 methods=['GET'])
def cities(state_id):
    """
    This route return a list of cities given by the status id
    """
    storage_t = type(storage).__name__
    state_obj = storage.get(State, state_id)
    if state_obj is not None:
        return jsonify([cit.to_dict() for cit in state_obj.cities])
    abort(404)


@app_views.route("/cities/<city_id>", strict_slashes=False, methods=['GET'])
def single_city(city_id):
    """
    Return the Json of a City by its id
    """
    citi = storage.get(City, city_id)
    if citi is not None:
        return jsonify(citi.to_dict())
    abort(404)


@app_views.route("/cities/<city_id>", strict_slashes=False, methods=['DELETE'])
def remove_city(city_id):
    """
    Handles the State remotion route,
    takes and id and uses storage to remove it
    """
    citi = storage.get(City, city_id)
    if citi is not None:
        storage.delete(citi)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route("/states/<state_id>/cities",
                 strict_slashes=False,
                 methods=['POST'])
def create_city(state_id):
    """
    Creates a new city in the State
    given by state_id
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    req = request.get_json()
    if not req or type(req) != dict:
        return jsonify(error="Not a JSON"), 400
    if "name" not in req:
        return jsonify(error="Missing name"), 400
    n_city = City(**req)
    n_city.state_id = state_id
    storage.new(n_city)
    storage.save()
    return jsonify(n_city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=['PUT'])
def update_city(city_id):
    """
    Update the city given by city_id
    returns error if there is no name or if request is not a proper dict
    """
    req = request.get_json()
    if not req:
        abort(400, "Not a JSON")
    city = storage.get(City, city_id)
    if city is not None:
        for key in req.keys():
            setattr(city, key, req[key])
        storage.save()
        return jsonify(city.to_dict()), 200
    abort(404)
