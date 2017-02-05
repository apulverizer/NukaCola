from flask import Flask
from app.api.views import api

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    app.register_blueprint(api, url_prefix='/outputs')
    return app

app = create_app('config')