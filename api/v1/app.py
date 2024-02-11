#!/usr/bin/python3
"""Nuestra app principal"""

from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv
from flask import jsonify

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_session(close):
    """Cierra sesión"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Admnistra un respuesta de error 404"""
    return jsonify({"error": "Not found"}), 404


if __name__ == '__main__':
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', '5000')
    app.run(host=host, port=port, threaded=True)
