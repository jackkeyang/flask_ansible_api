from flask import Flask
from config import *

def create_app(app_name):
    app = Flask(__name__)
    app.config.from_object(config[app_name])

    from api import api
    app.register_blueprint(api, url_prefix='/api')

    return app