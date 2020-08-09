#!/usr/bin/python3
"""
Amenities route for AirBnB clone v3 API v1
"""

from models import storage
from models.review import Review
from models.place import Place
from models.amenity import Amenity
from models.user import User
from api.v1.views import app_views
from flask import jsonify, make_response, abort, request, Response
import json


@app_views.route("/places/<place_id>/amenities", methods=['GET'])
def get_amenities(place_id):
    """
    Returns a list of amenities given by a place
    @place_id: place related to the amenities
    """
    storage_t = type(storage).__name__
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if storage_t == "DBStorage":
        return jsonify([am.to_dict() for am in place.amenities])
    else:
        amens = []
        for am_id in place.amenity_ids:
            am = storage.get(Amenity, am_id)
            if am is not None:
                amens.append(am.to_dict())
        resp = Response(json.dumps(amens, indent=2),
                        200,
                        mimetype="application/json")
        return resp


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=['DELETE'])
def remove_amenity_from_place(place_id, amenity_id):
    """
    Remove an amenity from a place
    Behaves differently depending on the storage engine its being used
    @place_id: place to update
    @amenity_id: amenity to remove
    """
    storage_t = type(storage).__name__
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if storage_t == "DBStorage":
        exists = False
        for amen in place.amenities:
            if amen.id == amenity_id:
                print("exists")
                place.amenities.remove(amen)
                for pl in amenity.place_amenities:
                    if pl.id == place.id:
                        amenity.place_amenities.remove(place)
                exists = True
        if not exists:
            abort(404)
        storage.save()
        return jsonify({}), 200
    else:
        if amenity_id in place.amenity_ids:
            del place.amenity_ids[place.amenity_ids.index(amenity_id)]
        else:
            abort(404)
        if place_id in amenity.place_id:
            del place.amenity_ids[place.amenity_ids.index(amenity_id)]
        storage.save()
        return jsonify({}), 200


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=['POST'])
def link_amenity_to_place(place_id, amenity_id):
    """
    Links an Amenity to a given place
    @place_id: the place to update
    @amenity_id: the amenity to be linked
    """
    storage_t = type(storage).__name__
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if storage_t == "DBStorage":
        amenities = place.amenities
        for am in amenities:
            if am.id == amenity_id:
                return jsonify(amenity.to_dict()), 200
        place.amenities.append(amenity)
        storage.save()
        return jsonify(amenity.to_dict()), 201
    else:
        if amenity_id in place.amenity_ids:
            return jsonify(amenity.to_dict()), 200
        place.amenity_ids.append(amenity.id)
        place.save()
        amenity.place_id.append(place.id)
        amenity.save()
        storage.save()
        return jsonify(amenity.to_dict()), 201
