#!/usr/bin/python3
"""Flask Application"""
from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS
from flasgger import Swagger

app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

app.config['SWAGGER'] = {
    'title': 'AirBnB clone Restful API',
    'uiversion': 3,
    'specs_route': '/apidocs/'
}
swagger = Swagger(app)

@app.teardown_appcontext
def close_db(error):
    """Close database"""
    storage.close()

@app.errorhandler(404)
def not_found(error):
    """404 Error handler"""
    return make_response(jsonify({'error': "Not found"}), 404)

if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', '5000')
    app.run(host=host, port=port, threaded=True)