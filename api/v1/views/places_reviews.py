#!/usr/bin/python3
"""Este módulo contiene todas las rutas para
nuestros hacer un CRUD con Review"""


from flask import jsonify, request, abort, make_response
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews', strict_slashes=False,
                 methods=['GET'])
def get_place_reviews(place_id):
    """Recupera la lista de todos los objetos de Review de un lugar"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    list_reviews = [review.to_dict() for review in place.reviews]
    return jsonify(list_reviews)


@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=['GET'])
def get_review(review_id):
    """Recupera un objeto de Review por su id"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_review(review_id):
    """Elimina un objeto review pr su id"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', strict_slashes=False,
                 methods=['POST'])
def create_review(place_id):
    """Crea un nuevo objeto de Review"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    if not isinstance(data, dict):
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    if 'user_id' not in data:
        return make_response(jsonify({'error': 'Missing user_id'}), 400)

    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404)

    if 'text' not in data:
        return make_response(jsonify({'error': 'Missing text'}), 400)

    data['place_id'] = place_id
    new_review = Review(**data)
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=['PUT'])
def update_review(review_id):
    """Actualiza un objeto de Review por su id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    data = request.get_json()
    if not isinstance(data, dict):
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
