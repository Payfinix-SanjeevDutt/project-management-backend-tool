from flask import Flask
from flask_cors import CORS

from .blueprints import register_blueprints
from .config import initconfig
from .database import initdb

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})
    initconfig(app)
    initdb(app)
    register_blueprints(app)
    return app