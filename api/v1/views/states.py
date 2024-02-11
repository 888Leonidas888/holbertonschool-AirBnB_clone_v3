#!usr/bin/python3
"""Este módulo contiene todas las rutas para
nuestros hacer un CRUD con State"""

from models.state import State
from api.v1.views import app_views
from models import storage
from flask import jsonify, request, abort


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def states():
    """Regresa una lista con todos los datos de cada State."""
    temp = [obj.to_dict() for obj in storage.all(State).values()]
    return jsonify(temp)

@app_views.route('/states', strict_slashes=False, methods=['POST'])
def create_state():
    """Crea un nuevo objeto Estado"""
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    elif "name" not in data:
        abort(400, "Missing name")
    else:
        new_state = State(**data)
        new_state.save()
        return jsonify(new_state.to_dict()), 201

@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def state(state_id):
    """Recupera un objeto de State por su id"""
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    else:
        abort(404)

@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def update_state(state_id):
    """Actualiza un objeto de estado por su id"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200

@app_views.route('/states/<state_id>', strict_slashes=False, methods=['DELETE'])
def delete_state(state_id):
    """Elimina un objeto de State por su id"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200
