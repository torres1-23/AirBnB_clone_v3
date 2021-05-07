#!/usr/bin/python3
"""This module defines a Flask Blueprint.

Usage:
    Add method to appviews blueprint to serve
    request to '/places/<place_id>/reviews' and
    '/reviews' route"""

from api.v1.views import app_views
from models import storage
from flask import request, jsonify, abort
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('places/<place_id>/reviews',
                 methods=['GET', 'POST'], strict_slashes=False)
def reviews_by_places(place_id):
    place_obj = storage.get(Place, place_id)
    if place_obj is None:
        abort(404)
    if request.method == 'GET':
        reviews_list = []
        for value in place_obj.reviews:
            reviews_list.append(value.to_dict())
        return jsonify(reviews_list)
    if request.method == 'POST':
        body_dict = request.get_json()
        if body_dict is None:
            abort(400, 'Not a JSON')
        try:
            user_id = body_dict["user_id"]
        except KeyError:
            abort(400, 'Missing user_id')
        user_obj = storage.get(User, user_id)
        if user_obj is None:
            abort(404)
        try:
            body_dict["text"]
        except KeyError:
            abort(400, 'Missing text')
        body_dict['text'] = city_id
        review_obj = Review(**body_dict)
        review_obj.save()
        return review_obj.to_dict(), 201


@app_views.route('reviews/<review_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def reviews(review_id):
    review_obj = storage.get(Review, review_id)
    if review_obj is None:
        abort(404)
    if request.method == 'GET':
        return review_obj.to_dict()
    if request.method == 'DELETE':
        review_obj.delete()
        storage.save()
        return {}
    if request.method == 'PUT':
        update_dict = request.get_json()
        if update_dict is None:
            abort(400, 'Not a JSON')
        ignore_list = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
        for element in ignore_list:
            try:
                del update_dict[element]
            except KeyError:
                pass
        for key, value in update_dict.items():
            setattr(review_obj, key, value)
        review_obj.save()
        return review_obj.to_dict()
