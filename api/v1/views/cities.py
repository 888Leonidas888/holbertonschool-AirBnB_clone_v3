#!/usr/bin/python3
"""Este módulo contiene todas las rutas para
nuestros hacer un CRUD con State"""

from models.state import State
from models.city import City
from api.v1.views import app_views
from models import storage
from flask import jsonify, request, abort, make_response


@app_views.route('/states/<state_id>/cities',
                 strict_slashes=False, methods=['GET'])
def get_cities_state(state_id):
    """Regresa una lista con todos los datos de las ciudades
    pertencientes aun Estado."""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    list_cities = [city.to_dict() for city in state.cities]
    return jsonify(list_cities)


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['GET'])
def get_city(city_id):
    """Recupera un objeto de City por su id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    else:
        return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_city(city_id):
    """Elimina un objeto de City por su id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities',
                 strict_slashes=False, methods=['POST'])
def create_city(state_id):
    """Crea un nuevo objeto City"""
    state = storage.get(State, state_id)

    if state is None:
        abort(404)

    data = request.get_json()
    if not isinstance(data, dict):
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    if "name" not in data:
        return make_response(jsonify({'error': 'Missing name'}), 400)

    data['state_id'] = state_id
    new_city = City(**data)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['PUT'])
def update_city(city_id):
    """Actualiza una ciudad por su id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    data = request.get_json()
    if not isinstance(data, dict):
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200
