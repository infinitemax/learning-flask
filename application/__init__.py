from flask import Flask
from flask_pymongo import PyMongo
from dotenv import load_dotenv

load_dotenv()
import os
MONGODB_URI = os.getenv("MONGODB_URI")

app = Flask(__name__)
app.config["SECRET_KEY"] = "957ba611c58ea25173e30377498ebf50bcfa4a7d"
app.config["MONGO_URI"] = MONGODB_URI

# set up mongodb
mongodb_client = PyMongo(app)
db = mongodb_client.db


from application import routes