#!/usr/bin/python3
"""Definition of the API server"""


from api.v1.views import app_views
from flask import Flask, jsonify, make_response
from flask_cors import CORS
from flasgger import Swagger, swag_from
from models import storage
from os import getenv


app = Flask(__name__)
CORS(app, origins='0.0.0.0', resources='/*')
swagger = Swagger(app)
swagger.template = swagger.load_swagger_file('../../docs/api.yml')
app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def closeStorageAfterRequest(error):
    """Close and reload the storage device between requests"""
    storage.close()
    storage.reload()


@app.errorhandler(404)
def error404(error):
    """Use a JSON rather than HTML response when a URL is not found"""
    return make_response(jsonify(error="Not found"), 404)


if __name__ == '__main__':
    app.run(
        host=getenv('HBNB_API_HOST', '0.0.0.0'),
        port=getenv('HBNB_API_PORT', 5000),
        threaded=True
    )
