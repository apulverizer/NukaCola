# -*- coding: UTF-8 -*-
from flask import Flask
from app.api.views import api
from flask_cors import CORS
from neopixel import *

def create_app(config):
    """
    Factory method to create an app instance using a config file
    """
    app = Flask(__name__)
    CORS(app)
    app.url_map.strict_slashes = False
    app.config.from_object(config)
    app.register_blueprint(api, url_prefix='/outputs')
    configure_outputs(app)
    return app


def configure_outputs(app):
    """
    Configures the leds via neopixel library
    :param app: the application instance
    :return:
    """
    # Create NeoPixel object with appropriate configuration.
    app.config['LEDS'] = Adafruit_NeoPixel(
      app.config['LED_COUNT'],
      app.config['LED_PIN'],
      app.config['LED_FREQ_HZ'],
      app.config['LED_DMA'],
      app.config['LED_INVERT'],
      app.config['LED_BRIGHTNESS'],
      app.config['LED_CHANNEL'],
      app.config['LED_STRIP']
    )
    # Intialize the library (must be called once before other functions).
    app.config['LEDS'].begin()
    # turn off all pixels
    for i in range(app.config['LEDS'].numPixels()):
        app.config['LEDS'].setPixelColor(i, Color(0, 0, 0))
    app.config['LEDS'].show()

app = create_app('config')
