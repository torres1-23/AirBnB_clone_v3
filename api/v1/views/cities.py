#!/usr/bin/python3
"""This module defines a Flask Blueprint.

Usage:
    Add method to appviews blueprint to serve
    request to '/states/<state_id>/cities' and
    '/cities' route"""

from api.v1.views import app_views
from models import storage
from flask import request, jsonify, abort
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities',
                 methods=['GET', 'POST'], strict_slashes=False)
def cities_by_states(state_id):
    state_obj = storage.get(State, state_id)
    if state_obj is None:
        abort(404)
    if request.method == 'GET':
        cities_list = []
        for value in state_obj.cities:
             cities_list.append(value.to_dict())
        return jsonify(cities_list)
    if request.method == 'POST':
        body_dict = request.get_json()
        if body_dict is None:
            abort(400, 'Not a JSON')
        try:
            body_dict["name"]
        except KeyError:
            abort(400, 'Missing name')
        body_dict['state_id'] = state_id
        city_obj = City(**body_dict)
        city_obj.save()
        return city_obj.to_dict(), 201


@app_views.route('cities/<city_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def cities(city_id):
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404)
    if request.method == 'GET':
        return city_obj.to_dict()
    if request.method == 'DELETE':
        city_obj.delete()
        storage.save()
        return {}
    if request.method == 'PUT':
        update_dict = request.get_json()
        if update_dict is None:
            abort(400, 'Not a JSON')
        ignore_list = ['id', 'state_id', 'created_at', 'updated_at']
        for element in ignore_list:
            try:
                del update_dict[element]
            except KeyError:
                pass
        for key, value in update_dict.items():
            setattr(city_obj, key, value)
        city_obj.save()
        return city_obj.to_dict()
