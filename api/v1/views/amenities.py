#!/usr/bin/python3
"""Este módulo contiene todas las rutas para
nuestros hacer un CRUD con Amenity"""

from models.amenity import Amenity
from api.v1.views import app_views
from models import storage
from flask import jsonify, request, abort, make_response


@app_views.route('/amenities', strict_slashes=False, methods=['GET'])
def get_amenities():
    """Regresa una lista con todos los datos de cada Amemity."""
    temp = [obj.to_dict() for obj in storage.all(Amenity).values()]
    return jsonify(temp)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False, methods=['GET'])
def get_amanities(amenity_id):
    """Recupera un objeto Amenity por su id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    else:
        return jsonify(amenity.to_dict())
    

@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_amenities(amenity_id):
    """Elimina un objeto Amenity por su id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', strict_slashes=False, methods=['POST'])
def create_amenities():
    """Crea un nuevo objeto Amenity"""
    data = request.get_json()
    if not isinstance(data, dict):
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    if "name" not in data:
        return make_response(jsonify({'error': 'Missing name'}), 400)

    new_state = Amenity(**data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('amenities/<amenity_id>', strict_slashes=False, methods=['PUT'])
def update_amenities(amenity_id):
    """Actualiza un objeto Amenity por su id."""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    data = request.get_json()
    if not isinstance(data, dict):
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
