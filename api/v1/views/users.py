#!/usr/bin/python3
"""Este módulo contiene todas las rutas para
nuestros hacer un CRUD con Amenity"""

from models.user import User
from api.v1.views import app_views
from models import storage
from flask import jsonify, request, abort, make_response


@app_views.route('/users', strict_slashes=False, methods=['GET'])
def get_user():
    """Regresa una lista con todos los datos de cada User."""
    temp = [obj.to_dict() for obj in storage.all(User).values()]
    return jsonify(temp)


@app_views.route('users/<user_id>', strict_slashes=False, methods=['GET'])
def get_user(user_id):
    """Recupera un objeto User por su id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    else:
        return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_user(user_id):
    """Elimina un objeto User por su id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def create_users():
    """Crea un nuevo objeto User"""
    data = request.get_json()
    if not isinstance(data, dict):
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    if "email" not in data:
        return make_response(jsonify({'error': 'Missing email'}), 400)

    if "password" not in data:
        return make_response(jsonify({'error': 'Missing password'}), 400)
    new_user = User(**data)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('users/<user_id>', strict_slashes=False, methods=['PUT'])
def update_user(user_id):
    """Actualiza un objeto User por su id."""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    data = request.get_json()
    if not isinstance(data, dict):
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    for key, value in data.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
