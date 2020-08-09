#!/usr/bin/python3
"""
Index route for AirBnB clone v3 API v1
"""


from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User



@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """
    This route return a success status in JSON format
    ---
    responses:
      200:
        description: Return OK if API is running
        content:
           application/json
        schema:
          type: object
          properties:
            status:
              type: string
              example: OK
    """
    return jsonify(status="OK"), 200


@app_views.route('/stats', methods=['GET'])
def count():
    """
    This route return number of all models
    ---
    responses:
      200:
          description: Return the count of all models
          content:
             application/json
          schema:
           type: object
           properties:
               amenities:
                   type: integer
                   example: 32
               cities:
                   type: integer
                   example: 34
               places:
                   type: integer
                   example: 65
               reviews:
                   type: integer
                   example: 84
               states:
                   type: integer
                   example: 35
               users:
                   type: integer
                   example: 91

    """
    return jsonify(amenities=storage.count(Amenity),
                   cities=storage.count(City),
                   places=storage.count(Place),
                   reviews=storage.count(Review),
                   states=storage.count(State),
                   users=storage.count(User))
