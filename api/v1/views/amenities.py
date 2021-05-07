#!/usr/bin/python3
"""This module defines a Flask Blueprint.

Usage:
    Add method to appviews blueprint to serve
    request to '/amenities' route"""
 
from api.v1.views import app_views
from models import storage
from flask import request, jsonify, abort
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET', 'POST'], strict_slashes=False)
def method():
    if request.method == 'GET':
        amenities_list = []
        amenities_dict = storage.all(Amenity)
        for value in amenities_dict.values():
            amenities_list.append(value.to_dict())
        return jsonify(amenities_list)
    if request.method == 'POST':
        body_dict = request.get_json()
        if body_dict is None:
            abort(400, 'Not a JSON')
        try:
            body_dict["name"]
        except KeyError:
            abort(400, 'Missing name')
        obj = Amenity(**body_dict)
        obj.save()
        return obj.to_dict(), 201


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def method_by_id(amenity_id):
    obj = storage.get(Amenity, amenity_id)
    if obj is None:
        abort(404)
    if request.method == 'GET':
        return obj.to_dict()
    if request.method == 'DELETE':
        obj.delete()
        storage.save()
        return {}
    if request.method == 'PUT':
        update_dict = request.get_json()
        if update_dict is None:
            abort(400, 'Not a JSON')
        ignore_list = ['id', 'created_at', 'updated_at']
        for element in ignore_list:
            try:
                del update_dict[element]
            except KeyError:
                pass
        for key, value in update_dict.items():
            setattr(obj, key, value)
        obj.save()
        return obj.to_dict()
