#!/usr/bin/python3
"""Este módulo contiene todas las rutas para
nuestros hacer un CRUD con State"""

from models.state import State
from api.v1.views import app_views
from models import storage
from flask import jsonify, request, abort, make_response


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def get_states():
    """Regresa una lista con todos los datos de cada State."""
    temp = [obj.to_dict() for obj in storage.all(State).values()]
    return jsonify(temp)


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def create_state():
    """Crea un nuevo objeto Estado"""
    data = request.get_json()
    if not isinstance(data, dict):
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    if "name" not in data:
        return make_response(jsonify({'error': 'Missing name'}), 400)

    new_state = State(**data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def get_state(state_id):
    """Recupera un objeto de State por su id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    else:
        return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def update_state(state_id):
    """Actualiza un objeto de estado por su id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    data = request.get_json()
    if not isinstance(data, dict):
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_state(state_id):
    """Elimina un objeto de State por su id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200
