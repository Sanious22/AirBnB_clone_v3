#!/usr/bin/python3
""" cities view api routes """

from models.base_model import BaseModel
from flask import Flask, abort, jsonify, make_response, request
from api.v1.views import app_views
import models


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def get_cities_belonging_to_states(state_id):
    """ return all city objects of a given state. """
    state = models.storage.get('State', state_id)
    if state is None:
        abort(404)
    return jsonify([city.to_dict() for city in state.cities])


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city_id(city_id):
    """ return single city matching id in JSON. """
    city = models.storage.get('City', city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """ delete city matching given id. """
    city = models.storage.get('City', city_id)
    if city is None:
        abort(404)
    city.delete()
    models.storage.save()
    return jsonify({})


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def create_city(state_id):
    """ create city attached to given state. """
    body = request.get_json(silent=True)
    if body is None:
        abort(400, jsonify(error="Not a JSON"))
    if 'name' not in body:
        abort(400, jsonify(error="Missing name"))
    state = models.storage.get('State', state_id)
    if state is None:
        abort(404)
    city = models.city.City(**body)
    city.state_id = state_id
    models.storage.new(city)
    models.storage.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """ update specific city object with given information. """
    body = request.get_json(silent=True)
    if body is None:
        abort(400, jsonify(error="Not a JSON"))
    city = models.storage.get('City', city_id)
    if city is None:
        abort(404)
    for key, value in body.items():
        if key not in ('id', 'state_id', 'created_at', 'updated_at'):
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict())
