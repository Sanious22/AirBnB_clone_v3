#!/usr/bin/python3
"""Module to allow examining the link between places and amenities"""


from api.v1.views import app_views
import flask
from models import storage
import os


@app_views.route('/places/<place_id>/amenities', methods=('GET',))
def api_getPlaceAmenities(place_id):
    """get the list of amenities at a given place"""
    place = storage.get('Place', place_id)
    if place is None:
        flask.abort(404)
    return flask.jsonify([amenity.to_dict() for amenity in place.amenities])


@app_views.route(
    '/places/<place_id>/amenities/<amenity_id>',
    methods=('DELETE',)
)
def api_removeAmenityFromPlace(place_id, amenity_id):
    """remove an amenity from a place"""
    place = storage.get('Place', place_id)
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None or place is None or amenity not in place.amenities:
        flask.abort(404)
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        place.amenities.remove(amenity)
    else:
        place.amenity_ids.remove(amenity.id)
    storage.save()
    return flask.jsonify({})


@app_views.route(
    '/places/<place_id>/amenities/<amenity_id>',
    methods=('POST',)
)
def api_addAmenityToPlace(place_id, amenity_id):
    """associate a new amenity with a place"""
    place = storage.get('Place', place_id)
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None or place is None:
        flask.abort(404)
    if amenity in place.amenities:
        return flask.jsonify(amenity.to_dict())
    place.amenities.append(amenity)
    storage.save()
    return flask.make_response(flask.jsonify(amenity.to_dict()), 201)
