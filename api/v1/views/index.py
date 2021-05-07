#!/usr/bin/python3
"""This module defines a Flask Blueprint.

Usage:
    Register this Blueprint to an app in order to serve
    request to '/status' and '/stats' routes"""

from api.v1.views import app_views
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    """Return status of response"""
    return ({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def stats():
    """Retrieves the number of each objects by type"""
    return({
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    })
