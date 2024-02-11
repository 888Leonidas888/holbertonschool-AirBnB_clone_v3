#!usr/bin/python3
"""Este módulo contiene todas las rutas para
nuestros hacer un CRUD con State"""

from models.state import State
from api.v1.views import app_views
from models import storage
from flask import jsonify


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def states():
    """Regresa una lista con todos los datos de cada State."""
    temp = [obj.to_dict() for obj in storage.all(State).values()]
    return jsonify(temp)

@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def state(state_id):
    state = storage.all(state_id)
    if state:
        return jsonify(state.to_dict())
    else:
        return 404