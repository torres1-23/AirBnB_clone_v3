#!/usr/bin/python3
"""This module defines a Flask Blueprint.

Usage:
    Add method to appviews blueprint to serve
    request to '/cities/<city_id>/places' and
    '/places' route"""

from api.v1.views import app_views
from models import storage
from flask import request, jsonify, abort
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places',
                 methods=['GET', 'POST'], strict_slashes=False)
def places_by_cities(city_id):
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404)
    if request.method == 'GET':
        places_list = []
        for value in city_obj.places:
            places_list.append(value.to_dict())
        return jsonify(places_list)
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
            body_dict["name"]
        except KeyError:
            abort(400, 'Missing name')
        body_dict['city_id'] = city_id
        place_obj = Place(**body_dict)
        place_obj.save()
        return place_obj.to_dict(), 201


@app_views.route('places/<place_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def places(place_id):
    place_obj = storage.get(Place, place_id)
    if place_obj is None:
        abort(404)
    if request.method == 'GET':
        return place_obj.to_dict()
    if request.method == 'DELETE':
        place_obj.delete()
        storage.save()
        return {}
    if request.method == 'PUT':
        update_dict = request.get_json()
        if update_dict is None:
            abort(400, 'Not a JSON')
        ignore_list = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
        for element in ignore_list:
            try:
                del update_dict[element]
            except KeyError:
                pass
        for key, value in update_dict.items():
            setattr(place_obj, key, value)
        place_obj.save()
        return place_obj.to_dict()
