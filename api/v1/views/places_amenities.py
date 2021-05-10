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
from models.amenity import Amenity
from os import getenv

STORAGE = getenv('HBNB_TYPE_STORAGE')


@app_views.route('places/<place_id>/amenities',
                 methods=['GET'], strict_slashes=False)
def amenities_by_places(place_id):
    """Serve amenities route"""
    place_obj = storage.get(Place, place_id)
    if request.method == 'GET':
        if place_obj is None:
            abort(404)
        all_amenities = storage.all(Amenity)
        if STORAGE == 'db':
            place_amenities = place_obj.amenities
        else:
            place_amen_ids = place_obj.amenities
            place_amenities = []
            for amen in place_amen_ids:
                response.append(storage.get(Amenity, amen))
        place_amenities = [
            obj.to_json() for obj in place_amenities
            ]
        return jsonify(place_amenities)


@app_views.route('places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE', 'POST'], strict_slashes=False)
def amenity(place_id, amenity_id):
    """Serve amenities route"""
    place_obj = storage.get(Place, place_id)
    amenity_obj = storage.get(Amenity, amenity_id)
    if place_obj is None:
        abort(404)
    if amenity_obj is None:
        abort(404)
    if request.method == 'DELETE':
        if (amenity_obj not in place_obj.amenities and
                amenity_obj.id not in place_obj.amenities):
            abort(404)
        if STORAGE == 'db':
            place_obj.amenities.remove(amenity_obj)
        else:
            place_obj.amenity_ids.pop(amenity_obj.id, None)
        place_obj.save()
        return jsonify({}), 200
    if request.method == 'POST':
        if (amenity_obj in place_obj.amenities or
                amenity_obj.id in place_obj.amenities):
            return jsonify(amenity_obj.to_json()), 200
        if STORAGE == 'db':
            place_obj.amenities.append(amenity_obj)
        else:
            place_obj.amenities = amenity_obj
        return jsonify(amenity_obj.to_json()), 201
