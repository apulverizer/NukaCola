# -*- coding: UTF-8 -*-
from flask import Flask
from app.api.views import api
import RPi.GPIO as GPIO

def create_app(config):
    """
    Factory method to create an app instance using a config file
    """
    app = Flask(__name__)
    app.config.from_object(config)
    app.register_blueprint(api, url_prefix='/outputs')
    configure_outputs(app)
    return app


def configure_outputs(app):
    """
    Configures the outputs usign RPi GPIO library
    :param app: the application instance
    :return:
    """
    GPIO.setmode(GPIO.BOARD)
    for id, pin in app.config['OUTPUTS'].items():
        GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)

app = create_app('config')