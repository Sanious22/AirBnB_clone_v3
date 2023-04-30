#!/usr/bin/python3
""" states view api """

from models.base_model import BaseModel
from flask import Flask, abort, jsonify, make_response, request
from api.v1.views import app_views
import models


@app_views.route('/states', methods=['GET'])
def get_state():
    """ retreive list of states and convert to JSON """
    return jsonify([
        state.to_dict()
        for state in models.storage.all('State').values()
    ])


@app_views.route('/states/<state_id>', methods=['GET'])
def get_state_id(state_id):
    """ retreive single state matching ID and return in JSON """
    state = models.storage.get('State', state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """ delete state matching given ID. """
    temp = models.storage.get('State', state_id)
    if temp is None:
        abort(404)
    temp.delete()
    models.storage.save()
    return jsonify({})


@app_views.route('/states', methods=['POST'])
def create_state():
    """ creates a new state object. """
    body = request.get_json(silent=True)
    if body is None:
        abort(400, jsonify(error="Not a JSON"))
    if 'name' not in body:
        abort(400, jsonify(error="Missing name"))
    state = models.state.State(**body)
    models.storage.new(state)
    models.storage.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """ update specific state object with new information. """
    body = request.get_json(silent=True)
    if body is None:
        abort(400, jsonify(error="Not a JSON"))
    state = models.storage.get('State', state_id)
    if state is None:
        abort(404)
    for key, value in body.items():
        if key not in ('created_at', 'updated_at', 'id'):
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict())
