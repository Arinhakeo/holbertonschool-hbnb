"""API package initialization"""
from flask import Flask
from flask_cors import CORS
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

@app.teardown_appcontext
def close_db(error):
    storage.close()

@app.errorhandler(404)
def not_found_error(error):
    return {"error": "Not found"}, 404