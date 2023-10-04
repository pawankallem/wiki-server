from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/scrape/*": {"origins": "http://localhost:5173"}})

from app import routes


