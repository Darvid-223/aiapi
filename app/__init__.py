from flask import Flask
from flask_cors import CORS

app = Flask(
    __name__,
    template_folder="templates",  # pekar på app/templates/
    static_folder="static"        # pekar på app/static/
)

CORS(app)

from app import routes
