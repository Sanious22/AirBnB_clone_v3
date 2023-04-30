#!/usr/bin/python3
"""Module for creating, updating and deleting users' reviews of places"""


from api.v1.views import app_views
import flask
import models
import models.review


@app_views.route('/places/<place_id>/reviews', methods=('GET',))
def api_getReviewsOfPlace(place_id):
    """List the reviews of a given place"""
    place = models.storage.get('Place', place_id)
    if place is None:
        flask.abort(404)
    return flask.jsonify([review.to_dict() for review in place.reviews])


@app_views.route('/reviews/<review_id>', methods=('GET',))
def api_getReview(review_id):
    """Get information about a review given its ID"""
    review = models.storage.get('Review', review_id)
    if review is None:
        flask.abort(404)
    return flask.jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=('DELETE',))
def api_deleteReview(review_id):
    """Delete a review given its ID"""
    review = models.storage.get('Review', review_id)
    if review is None:
        flask.abort(404)
    review.delete()
    models.storage.save()
    return flask.jsonify({})


@app_views.route('/places/<place_id>/reviews', methods=('POST',))
def api_addReviewToPlace(place_id):
    """Add a new review to an existing place"""
    place = models.storage.get('Place', place_id)
    if place is None:
        flask.abort(404)
    body = flask.request.get_json(silent=True)
    if body is None:
        return flask.make_response(flask.jsonify(error='Not a JSON'), 400)
    if 'user_id' not in body:
        return flask.make_response(flask.jsonify(error='Missing user_id'), 400)
    user = models.storage.get('User', body['user_id'])
    if user is None:
        flask.abort(404)
    if 'text' not in body:
        return flask.make_response(flask.jsonify(error='Missing text'), 400)
    review = models.review.Review(**body)
    review.place_id = place_id
    models.storage.new(review)
    models.storage.save()
    return flask.make_response(flask.jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=('PUT',))
def api_updateReview(review_id):
    """Update an existing review"""
    review = models.storage.get('Review', review_id)
    if review is None:
        flask.abort(404)
    body = flask.request.get_json(silent=True)
    if body is None:
        return flask.make_response(flask.jsonify(error='Not a JSON'), 400)
    for k, value in body.items():
        if k not in ('id', 'user_id', 'place_id', 'created_at', 'updated_at'):
            setattr(review, k, value)
    return flask.jsonify(review.to_dict())
