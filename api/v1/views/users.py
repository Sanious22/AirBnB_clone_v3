#!/usr/bin/python3
""" users view api """

from models.base_model import BaseModel
from flask import Flask, abort, jsonify, make_response, request
from api.v1.views import app_views
import models


@app_views.route('/users', methods=['GET'])
def get_users():
    """ retreive a list of users and convert to JSON. """
    return jsonify([
        users.to_dict()
        for users in models.storage.all('User').values()
        ])


@app_views.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """ retreive a single user matching given ID and return in JSON. """
    user = models.storage.get('User', user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """ delete user matching given id. """
    temp = models.storage.get('User', user_id)
    if temp is None:
        abort(404)
    temp.delete()
    models.storage.save()
    return jsonify({})


@app_views.route('/users', methods=['POST'])
def create_user():
    """ create a new user object. """
    body = request.get_json(silent=True)
    if body is None:
        abort(400, jsonify(error="Not a JSON"))
    if 'email' not in body:
        abort(400, jsonify(error="Missing email"))
    if 'password' not in body:
        abort(400, jsonify(error="Missing password"))
    user = models.user.User(**body)
    models.storage.new(user)
    models.storage.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """ update user object with new information. """
    body = request.get_json(silent=True)
    if body is None:
        abort(400, jsonify(error="Not a JSON"))
    user = models.storage.get('User', user_id)
    if user is None:
        abort(404)
    for key, value in body.items():
        if key not in ('id', 'email', 'created_at', 'updated_at'):
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict())
