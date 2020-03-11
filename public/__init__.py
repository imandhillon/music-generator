import os
from flask import Flask
from flask_cors import CORS

import lstmnet
from lstmnet import Singleton

app = Flask(__name__)
app.secret_key = "super_secret_key"

CORS(app)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 35 * 1024 * 1024


@app.before_first_request
def instantiate_model():
    model_manager = Singleton()
    model_manager.get_model()