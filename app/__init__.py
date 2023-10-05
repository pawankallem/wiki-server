from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

PY_ENV = os.getenv("PY_ENV")
LOCAL_URL = os.getenv("LOCAL_URL")
PROD_URL = os.getenv("PROD_URL")

if PY_ENV == "local":
    MY_URL = LOCAL_URL
elif PY_ENV == "prod":
    MY_URL = PROD_URL

app = Flask(__name__)
CORS(app, resources={
    r"/scrape/*": {"origins": MY_URL},
    r"/suggestion/*": {"origins": MY_URL}
})

from app import routes


