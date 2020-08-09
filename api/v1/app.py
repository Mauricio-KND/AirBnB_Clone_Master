#!/usr/bin/python3
"""
Flask Application server with view Blueprint
"""


from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify
from flask_cors import CORS
from flasgger import Swagger
import os


app = Flask(__name__)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
swagger = Swagger(app)


@app.errorhandler(404)
def page_not_found(e):
    """
    Defines not found json response
    ---
    responses:
      404:
         description: Not found
         examples:
           error: 'Not found'
    """
    print("Handling Error")
    return jsonify(error="Not found"), 404


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


if __name__ == '__main__':
    app.register_blueprint(app_views)
    host = os.getenv("HBNB_API_HOST")
    print(type(host), host)
    port = os.getenv("HBNB_API_PORT")
    app.run(host=host if host is not None else '0.0.0.0',
            port=port if port is not None else '5000',
            threaded=True)
