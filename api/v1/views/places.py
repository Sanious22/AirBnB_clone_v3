#!/usr/bin/python3
"""Module for displaying and searching through places for rent"""


from api.v1.views import app_views
import flask
import models
import models.place


@app_views.route('/cities/<city_id>/places', methods=('GET',))
def api_getPlacesInCity(city_id):
    """Get the places for rent in a city"""
    city = models.storage.get('City', city_id)
    if city is None:
        flask.abort(404)
    return flask.jsonify([place.to_dict() for place in city.places])


@app_views.route('/places/<place_id>', methods=('GET',))
def api_getPlace(place_id):
    """Get a place by ID"""
    place = models.storage.get('Place', place_id)
    if place is None:
        flask.abort(404)
    return flask.jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=('DELETE',))
def api_deletePlace(place_id):
    """Delete a place"""
    place = models.storage.get('Place', place_id)
    if place is None:
        flask.abort(404)
    place.delete()
    models.storage.save()
    return flask.jsonify({})


@app_views.route('/cities/<city_id>/places', methods=('POST',))
def api_addPlaceToCity(city_id):
    """Create a new place and put it in an existing city"""
    city = models.storage.get('City', city_id)
    if city is None:
        flask.abort(404)
    body = flask.request.get_json(silent=True)
    if body is None:
        return flask.make_response(flask.jsonify(error='Not a JSON'), 400)
    if 'user_id' not in body:
        return flask.make_response(flask.jsonify(error='Missing user_id'), 400)
    user = models.storage.get('User', body['user_id'])
    if user is None:
        flask.abort(404)
    if 'name' not in body:
        return flask.make_response(flask.jsonify(error='Missing name'), 400)
    place = models.place.Place(**body)
    place.city_id = city_id
    models.storage.new(place)
    models.storage.save()
    return flask.make_response(flask.jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=('PUT',))
def api_updatePlace(place_id):
    """Update an existing place"""
    place = models.storage.get('Place', place_id)
    if place is None:
        flask.abort(404)
    body = flask.request.get_json(silent=True)
    if body is None:
        return flask.make_response(flask.jsonify(error='Not a JSON'), 400)
    for key, value in body.items():
        if key not in ('id', 'user_id', 'city_id', 'created_at', 'updated_at'):
            setattr(place, key, value)
    place.save()
    return flask.jsonify(place.to_dict())


@app_views.route('/places_search', methods=('POST',))
def api_searchPlaces():
    """Search through places"""
    body = flask.request.get_json(silent=True)
    if body is None:
        return flask.make_response(flask.jsonify(error="Not a JSON"), 400)
    places = models.storage.all('Place').values()
    if 'states' in body and len(body['states']) > 0:
        places = [
            place for place in places
            if place.city.state.id in body['states']
        ]
    if 'cities' in body and len(body['cities']) > 0:
        places = [
            place for place in places
            if place.city.id in body['cities']
        ]
    if 'amenities' in body and len(body['amenities']) > 0:
        amenities = set(body['amenities'])
        places = [
            place for place in places
            if amenities - set(am.id for am in place.amenities) == set()
        ]
    return flask.jsonify([place.to_dict() for place in places])
