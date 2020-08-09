#!/usr/bin/python3
"""
Amenities route for AirBnB clone v3 API v1
"""

from models import storage
from models.amenity import Amenity
from api.v1.views import app_views
from flask import jsonify, make_response, abort, request
import json


@app_views.route('/amenities',
                 strict_slashes=False,
                 methods=['GET'])
def amenities():
    """
    This route retrieves the list of all amenity objects
    ---
    responses:
      200:
        description: return the list of all amenities
        schema:
          type: object
          properties:
            __class__:
              type: string
              example: 'Amenity'
            created_at:
              type: string
              example: '2017-03-25T02:17:06.000000'
            id:
              type: string
              example: 'acsd87asdfsacd6sdfadsfda8d'
            name:
              type: string
              example: 'Smoke detector'
            updated_at:
              type: string
              example: '2017-03-25T02:17:06.000000'

    """
    amenities = storage.all(Amenity)
    amenities_list = []
    for amenity in amenities.values():
        amenities_list.append(amenity.to_dict())
    return jsonify(amenities_list), 200


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False,
                 methods=['GET'])
def amenity_by_id(amenity_id):
    """
    This route retrieves a amenity object
    @amenity_id: id of amenity
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return jsonify(error="Not found"), 404
    return jsonify(amenity.to_dict()), 200


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False,
                 methods=['DELETE'])
def del_amenity(amenity_id):
    """
    This route delete a amenity
    @amenity_id: id of amenity that will be deleted
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return jsonify(error="Not found"), 404
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities',
                 strict_slashes=False,
                 methods=['POST'])
def create_amenity():
    """
    This route create a new amenity
    Require at least name
    """
    req = request.get_json()
    if req:
        if 'name' in req:
            new_amenity = Amenity(**req)
            storage.new(new_amenity)
            storage.save()
            return jsonify(new_amenity.to_dict()), 201
        else:
            return jsonify(error="Missing name"), 400
    return jsonify(error="Not a JSON"), 400


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False,
                 methods=['PUT'])
def update_amenity(amenity_id):
    """
    This route update a amenity
    @amenity_id: id of Amenity that will be updated
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return jsonify(error="Not found"), 404
    req = request.get_json()
    if req is None:
        return jsonify(error="Not a JSON"), 400
    for key, value in req.items():
            setattr(amenity, key, value)
    storage.save()
    return jsonify(amenity.to_dict()), 200
