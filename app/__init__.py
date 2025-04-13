from flask import Flask
from flask_cors import CORS

# Skapa en Flask-app med angivna mall- och statiska mappar
# och aktivera CORS för att tillåta korsdomänförfrågningar.
app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

CORS(app)

from app import routes
