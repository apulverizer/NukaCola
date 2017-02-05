from flask import Flask
from app.api.views import api
import RPi.GPIO as GPIO

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    app.register_blueprint(api, url_prefix='/outputs')
    configure_outputs()
    return app


def configure_outputs():
    GPIO.setmode(GPIO.BOARD)
    for id, pin in app.config['OUTPUTS'].items():
        GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)

app = create_app('config')