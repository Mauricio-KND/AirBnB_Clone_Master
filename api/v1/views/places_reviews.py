#!/usr/bin/python3
"""
Reviews route for AirBnB clone v3 API v1
"""

from models import storage
from models.review import Review
from models.place import Place
from models.user import User
from api.v1.views import app_views
from flask import jsonify, make_response, abort, request
import json


@app_views.route("/places/<place_id>/reviews",
                 strict_slashes=False,
                 methods=['GET'])
def get_reviews(place_id):
    """
    Returns a list of reviews by a given place
    @place_id: id of the place that holds the reviews
    ---
    get:
      parameters:
        - in: path
          name: place_id
          description: place id to get the reviews
          schema:
            type: string
          required: true
    responses:
      200:
        description: return a list of reviews for the given place
        schema:
          type: array
          items:
            type: object
            properties:
              __class__:
                type: string
                example: Review
              created_at:
                type: string
                example: 2017-03-25T02:17:07.000000
              id:
                type: string
                example: 87sfda8sfa8dsau8
              place_id:
                type: string
                example: dcascsa87dascin
              user_id:
                type: string
                example: "dsadsdads"
              text:
                type: string
                example: nice place i love it
              update_at:
                type: string
                example: 2017-03-25T02:17:07.000000
      400:
        description: 404 if no reviews are found
        schema:
          type: object
          properties:
            status:
              type: string
              example: Not found
        
    """
    # print('Get Reviews')
    place = storage.get(Place, place_id)
    # print(place)
    if place is None:
        abort(404)
    return jsonify([rev.to_dict() for rev in place.reviews])


@app_views.route("/reviews/<review_id>", strict_slashes=False, methods=['GET'])
def get_review(review_id):
    """
    Returns a review by a given id
    @review_id of the review to return
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>",
                 strict_slashes=False, methods=['DELETE'])
def delete_review(review_id):
    """
    Deletes a review by a given id
    @review_id of the review to return
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews",
                 strict_slashes=False, methods=['POST'])
def post_review(place_id):
    """
    Creates a review by a given id
    @place_id of the review to be created
    """
    req = request.get_json()
    if not req or type(req) != dict:
        return jsonify(error="Not a JSON"), 400
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if "user_id" not in req:
        return jsonify(error="Missing user_id"), 400
    user = storage.get(User, req['user_id'])
    if user is None:
        abort(404)
    if "text" not in req:
        return jsonify(error="Missing text"), 400
    review = Review(**req)
    review.place_id = place_id
    storage.new(review)
    storage.save()
    return jsonify(review.to_dict()), 201


@app_views.route("/reviews/<review_id>", strict_slashes=False, methods=['PUT'])
def update_review(review_id):
    """
    Updates a review by a given id
    @review_id of the review to update
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    req = request.get_json()
    if req is None or type(req) != dict:
        return jsonify(error="Not a JSON"), 400
    for key in req.keys():
        setattr(review, key, req[key])
    storage.save()
    return jsonify(review.to_dict()), 200
