#!/usr/bin/python3
"""Nuestra primera respuesta"""

from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', strict_slashes=False)
def status():
    """Nuestra primera salida exitosa con un JSON"""
    return jsonify({"status": "OK"})
