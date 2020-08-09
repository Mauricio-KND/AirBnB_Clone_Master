#!/usr/bin/python3
"""
Place route for AirBnB clone v3 API v1
"""

from models import storage
from models.city import City
from models.place import Place
from models.state import State
from models.user import User
from api.v1.views import app_views
from flask import jsonify, make_response, abort, request, Response
import json


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False,
                 methods=['GET'])
def get_places(city_id):
    """
    This route retrieves the list of all place objects of a city
    """
    city = storage.get(City, city_id)
    if city is None:
        return jsonify(error="Not found"), 404
    print(city.places)
    places = city.places
    places_list = []
    if places is not None:
        for place in places:
            places_list.append(place.to_dict())
    return jsonify(places_list), 200


@app_views.route('/places/<place_id>',
                 strict_slashes=False,
                 methods=['GET'])
def place_by_id(place_id):
    """
    This route retrieves a place object
    @place_id: id of place
    """
    place = storage.get(Place, place_id)
    if place is None:
        return jsonify(error="Not found"), 404
    return jsonify(place.to_dict()), 200


@app_views.route('/places/<place_id>',
                 strict_slashes=False,
                 methods=['DELETE'])
def del_place(place_id):
    """
    This route delete a place
    @place_id: id of place that will be deleted
    """
    place = storage.get(Place, place_id)
    if place is None:
        return jsonify(error="Not found"), 404
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False,
                 methods=['POST'])
def create_place(city_id):
    """
    This route create a new place
    @city_id: id of city to linked the place
    Require at least name and user_id
    Return the new Place object
    """
    storage_t = type(storage).__name__
    req = request.get_json()
    if req:
        city = storage.get(City, city_id)
        if city is None:
            return jsonify(error="Not found"), 404
        if 'user_id' in req:
            user = storage.get(User, req['user_id'])
            if user is None:
                return jsonify(error="Not found"), 404
        else:
            return jsonify(error="Missing user_id"), 400
        if 'name' in req:
            new_place = Place(**req)
            new_place.city_id = city_id
            if storage_t != "DBStorage":
                city.places_ids.append(new_place.id)
            storage.new(new_place)
            storage.save()
            return jsonify(new_place.to_dict()), 201
        else:
            return jsonify(error="Missing name"), 400
    return jsonify(error="Not a JSON"), 400


@app_views.route('/places/<place_id>',
                 strict_slashes=False,
                 methods=['PUT'])
def update_place(place_id):
    """
    This route update a place
    @place_id: id of place that will be updated
    """
    place = storage.get(Place, place_id)
    if place is None:
        return jsonify(error="Not found"), 404
    req = request.get_json()
    if req is None:
        return jsonify(error="Not a JSON"), 400
    for key, value in req.items():
        setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200


def print_place(place, typo):
    """
    Prints a Place Obj
    """
    if typo == "json":
        print('\n\033[33m', place["name"],
              '\n\t\033[34m',
              place["id"], '\033[0m')
    else:
        print('\n\033[33m', place.name, '\n\t\033[34m', place.id, '\033[0m\n')
        # , [am.name for am in place.amenities])


def filter_by_amenities(places, amenities):
    """
    Filter places by amenities
    """
    if len(amenities) == 0:
      return places
    filtered_places = []
    for place in places:
        pl_amens = [am.id for am in place.amenities]
        append = True
        for am in amenities:
            if am not in pl_amens:
                append = False
        if append:
            filtered_places.append(place)
    return filtered_places


@app_views.route("/places_search", methods=['POST'], strict_slashes=False)
def retrieve_search():
    """
    Return a list of places linked to the request data
    all places by cities in states and containing all amenities
    ---
    post:
      summary: 'Creates a new user.'
      consumes:
        - application/json
      parameters:
        - in: body
          name: body
          description: Filters to apply.
          schema:
            type: object
            properties:
              amenities:
                type: array
                items:
                  type: string
              states:
                type: array
                items:
                  type: string
              cities:
                type: array
                items:
                  type: string
    responses:
      200:
        description: Places filtered
        schema:
          type: array
          items:
            type: object
            properties:
              __class__:
                type: string
                example: Place
              description:
                type: string
                example: Comfortable bogaloo at the middel of the ocean
              name:
                type: string
                example: 42GVT
              max_guest:
                type: integer
                example: 2
              city_id:
                type: string
                example: 9231h2u3h12u9319nc
              number_bathrooms:
                type: integer
                example: 1
              number_rooms:
                type: integer
                example: 1
              owner:
                type: string
                example: Grandma Lily
              price_by_night:
                type: integer
                example: 90
              user_id:
                type: string
                example: 9283huf92b3fb32932
              updated_at:
                type: string
                example: 2017-03-25T02:17:06.000000
              created_at:
                type: string
                example: 2017-03-25T02:17:06.000000
    """
    print("requesting places")
    try:
        # print(dir(request))
        # print(request.headers)
        # args = request.args 
        # print(args)
        # print(request.mimetype)
        try:
            js = request.get_json()
        except Exception as e:
            print(e)
            js = {}
        if js is None or type(js) != dict:
            print('Data is not a Json')
            return jsonify(error="Not a JSON"), 400
        states = js["states"] if "states" in js else []
        cities = js["cities"] if "cities" in js else []
        amenities = js["amenities"] if "amenities" in js else []
        conds = [
            True if len(states) == 0 else False,
            True if len(cities) == 0 else False,
            True if len(amenities) == 0 else False
        ]
        print(conds)
    except Exception as e:
        print(e)
    if all(conds):
        print("return all places")
        places = storage.all(Place)
        all_places = []
        try:
            for place in places.values():
                pl = place.to_dict()
                user = storage.get_user(pl['user_id'])
                owner = user.first_name + ' ' + user.last_name
                pl['owner'] = owner
                all_places.append(pl)
            return jsonify(all_places), 200
        except Exception as e:
            print(e)
    s_places = []
    if len(states) > 0:
        for st_id in states:
            st = storage.get(State, st_id)
            if st is not None:
                for ci in st.cities:
                    for pla in ci.places:
                        s_places.append(pla)
    c_places = []
    if len(cities) > 0:
        for ci_id in cities:
            ci = storage.get(City, ci_id)
            if ci is not None:
                for pl in ci.places:
                    c_places.append(pl)
    f_places = []
    f_places.extend(s_places)
    f_places.extend(c_places)
    # print("\033[31mStates Places\033[0m")
    # for pl in s_places:
    #     print_place(pl, "Obj")
    # print("\033[31mCities Places\033[0m")
    # for pl in c_places:
    #     print_place(pl, "Obj")
    if len(amenities) > 0:
        f_places = filter_by_amenities(f_places, amenities)
        print("\033[31mFiltered by Amenities\033[0m")
        for pl in f_places:
            print_place(pl, "Obj")
        all_places = storage.all(Place)
        f_places.extend(filter_by_amenities(all_places.values(), amenities))
    print('places length', len(f_places))
    resp = []
    for pl in f_places:
        dic = pl.to_dict()            
        user = storage.get_user(dic['user_id'])
        owner = user.first_name + ' ' + user.last_name
        dic['owner'] = owner
        if "amenities" in dic:
            del dic["amenities"]
        resp.append(dic)
    # print(resp)
    return jsonify(resp), 200
