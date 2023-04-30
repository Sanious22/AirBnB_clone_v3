#!/usr/bin/python3
""" amenities view api commands/routes """

from models.base_model import BaseModel
from flask import Flask, abort, jsonify, make_response, request
from api.v1.views import app_views
import models


@app_views.route('/amenities', methods=['GET'])
def get_amenities():
    """ retreive list of amenities and convert to JSON. """
    return jsonify([
        amenity.to_dict()
        for amenity in models.storage.all('Amenity').values()
    ])


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenities_id(amenity_id):
    """ retreive single amenity with matching ID and return in JSON. """
    amenity = models.storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """ delete amenity with given ID. """
    temp = models.storage.get('Amenity', amenity_id)
    if temp is None:
        abort(404)
    temp.delete()
    models.storage.save()
    return jsonify({})


@app_views.route('/amenities', methods=['POST'])
def create_amenity():
    """ create a new amenity object. """
    body = request.get_json(silent=True)
    if body is None:
        abort(400, jsonify(error="Not a JSON"))
    if 'name' not in body:
        abort(400, jsonify(error="Missing name"))
    amenity = models.amenity.Amenity(**body)
    models.storage.new(amenity)
    models.storage.save()
    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """ update specific amenity object with new information. """
    amenity = models.storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)
    body = request.get_json(silent=True)
    if body is None:
        abort(400, jsonify(error="Not a JSON"))
    for key, value in body.items():
        if key not in ('id', 'created_at', 'updated_at'):
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict())
