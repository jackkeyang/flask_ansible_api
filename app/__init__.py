from flask import Flask
from flask_redis import FlaskRedis
from config import *

redis_store = FlaskRedis()

def create_app(app_name):
    app = Flask(__name__)
    app.config.from_object(config[app_name])
    
    redis_store.init_app(app)

    from app.views import view
    app.register_blueprint(view.mod, url_prefix='/api')

    return app