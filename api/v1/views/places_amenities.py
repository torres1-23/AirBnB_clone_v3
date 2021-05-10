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
    list_amenities = []
    if place_obj is None:
        abort(404)
    if STORAGE == 'db':
        amenities = storage.all(Amenity)
        for obj in amenities:
            list_amenities.append(obj.to_json())
    else:
        amenities_id = place_obj.amenities
        for id in amenities_id:
            obj = storage.get(Amenity, id)
            list_amenities.append(obj.to_dict())
    return jsonify(list_amenities)


@app_views.route('places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE', 'POST'], strict_slashes=False)
def amenity(place_id, amenity_id):
    """Serve amenities route"""
    place_obj = storage.get('Place', place_id)
    amenity_obj = storage.get('Amenity', amenity_id)
    if place_obj is None:
        abort(404, 'Not found')
    if amenity_obj is None:
        abort(404, 'Not found')
    if request.method == 'DELETE':
        if (amenity_obj not in place_obj.amenities and
                amenity_obj.id not in place_obj.amenities):
            abort(404, 'Not found')
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
