#!/usr/bin/python3
"""Este módulo contiene todas las rutas para
nuestros hacer un CRUD con Place."""

from models.place import Place
from models.city import City
from models.user import User
from api.v1.views import app_views
from models import storage
from flask import jsonify, request, abort, make_response


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False, methods=['GET'])
def get_places_cities(city_id):
    """Regresa una lista con todos los datos de los lugares
    pertencientes a una Ciudad."""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    places = storage.all(Place).values()
    list_places = [place.to_dict() for place in places
                   if place.city_id == city_id]
    return jsonify(list_places)


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['GET'])
def get_place(place_id):
    """Recupera un objeto de City por su id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    else:
        return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_place(place_id):
    """Elimina un objeto de Place por su id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False, methods=['POST'])
def create_place(city_id):
    """Crea un nuevo objeto City"""
    city = storage.get(City, city_id)

    if city is None:
        abort(404)

    data = request.get_json()
    if not isinstance(data, dict):
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    if "name" not in data:
        return make_response(jsonify({'error': 'Missing name'}), 400)

    if "user_id" not in data:
        return make_response(jsonify({'error': 'Missing user_id'}), 400)

    user = storage.get(User, data['user_id'])

    if user is None:
        abort(404)

    data['city_id'] = city_id
    new_place = Place(**data)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['PUT'])
def update_place(place_id):
    """Actualiza una ciudad por su id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    data = request.get_json()
    if not isinstance(data, dict):
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200
