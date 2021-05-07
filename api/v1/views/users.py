#!/usr/bin/python3
"""This module defines a Flask Blueprint.

Usage:
    Add method to appviews blueprint to serve
    request to '/users' route"""

from api.v1.views import app_views
from models import storage
from flask import request, jsonify, abort
from models.user import User


@app_views.route('/users', methods=['GET', 'POST'], strict_slashes=False)
def users():
    if request.method == 'GET':
        users_list = []
        users_dict = storage.all(User)
        for value in users_dict.values():
            users_list.append(value.to_dict())
        return jsonify(users_list)
    if request.method == 'POST':
        body_dict = request.get_json()
        if body_dict is None:
            abort(400, 'Not a JSON')
        try:
            body_dict["email"]
        except KeyError:
            abort(400, 'Missing email')
        try:
            body_dict["password"]
        except KeyError:
            abort(400, 'Missing password')
        obj = User(**body_dict)
        obj.save()
        return obj.to_dict(), 201


@app_views.route('/users/<user_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def users_by_id(user_id):
    obj = storage.get(User, user_id)
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
        ignore_list = ['id', 'email', 'created_at', 'updated_at']
        for element in ignore_list:
            try:
                del update_dict[element]
            except KeyError:
                pass
        for key, value in update_dict.items():
            setattr(obj, key, value)
        obj.save()
        return obj.to_dict()
