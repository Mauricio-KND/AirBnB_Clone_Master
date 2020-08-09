#!/usr/bin/python3
"""
States route for AirBnB clone v3 API v1
"""

from models import storage
from models.state import State
from api.v1.views import app_views
from flask import jsonify, make_response, abort, request
import json


@app_views.route('/states',
                 strict_slashes=False,
                 methods=['GET'])
def states():
    """
    This route retrieves the list of all State objects
    """
    states = storage.all(State)
    states_list = []
    for state in states.values():
        states_list.append(state.to_dict())
    return jsonify(states_list), 200


@app_views.route('/states/<state_id>',
                 strict_slashes=False,
                 methods=['GET'])
def state_by_id(state_id):
    """
    This route retrieves a State object
    @state_id: id of State
    """
    state = storage.get(State, state_id)
    if state is None:
        return jsonify(error="Not found"), 404
    return jsonify(state.to_dict()), 200


@app_views.route('/states/<state_id>',
                 strict_slashes=False,
                 methods=['DELETE'])
def del_state(state_id):
    """
    This route delete a state
    @state_id: id of State that will be deleted
    """
    state = storage.get(State, state_id)
    if state is None:
        return jsonify(error="Not found"), 404
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states',
                 strict_slashes=False,
                 methods=['POST'])
def create_state():
    """
    This route create a new state
    Require at least name
    """
    req = request.get_json()
    if req:
        if 'name' in req:
            new_state = State(**req)
            storage.new(new_state)
            storage.save()
            return jsonify(new_state.to_dict()), 201
        else:
            return jsonify(error="Missing name"), 400
    return jsonify(error="Not a JSON"), 400


@app_views.route('/states/<state_id>',
                 strict_slashes=False,
                 methods=['PUT'])
def update_state(state_id):
    """
    This route update a state
    """
    state = storage.get(State, state_id)
    if state is None:
        return jsonify(error="Not found"), 404
    req = request.get_json()
    if req is None:
        return jsonify(error="Not a JSON"), 400
    for key, value in req.items():
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200
