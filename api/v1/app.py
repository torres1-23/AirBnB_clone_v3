#!/usr/bin/python3
"""This module starts a Flask web application.

Usage:
    Run this script with: 'python3 -m app.py'
    to start a web server running on
    'http://<HBNB_API_HOST>:<HBNB_API_PORT>/'"""

from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv

HBNB_API_HOST = getenv('HBNB_API_HOST', '0.0.0.0')
HBNB_API_PORT = getenv('HBNB_API_PORT', '5000')
app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exc):
    """Teardown to remove the SQL session
    in db mode or reload the storage in fs mode"""
    storage.close()


@app.errorhandler(404)
def notfound(error):
    return {"error": "Not found"}, 404

if __name__ == "__main__":
    app.run(HBNB_API_HOST, HBNB_API_PORT)
