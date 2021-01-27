from flask import Flask
from flask_redis import FlaskRedis
from celery import Celery
from config import *
from celeryconfig import *

celery = Celery(__name__, broker=BROKER_URL, backend=RESULT_BACKEND, include=['celery_task.task'])
redis_store = FlaskRedis()

def create_app(app_name):
    app = Flask(__name__)
    app.config.from_object(config[app_name])

    init_celery(app)
    redis_store.init_app(app)

    from app.views import view
    app.register_blueprint(view.mod, url_prefix='/api')

    return app

def init_celery(app):
    celery.config_from_object('celeryconfig')

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    
    celery.Task = ContextTask