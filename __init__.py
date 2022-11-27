from flask import Flask

from .env import *
from .mongodb.mongo_connect import mongo
from .routes.main import main

# create flask app
app = Flask(__name__)

# config for file 
MAX_CONTENT_ALLOWED = 16 * 1000 * 1000
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_ALLOWED

# config database & start mongose
app.config['MONGO_URI'] = f'mongodb+srv://{usr}:{pwd}@cluster0.nbpt6ub.mongodb.net/{db}?retryWrites=true&w=majority'
mongo.init_app(app)

# attack blueprint from routes
app.register_blueprint(main)