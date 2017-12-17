# -*- coding: UTF-8 -*-
import struct
from flask import Blueprint, jsonify
from flask import current_app, request
from neopixel import *

api = Blueprint('api', __name__)


def raw_color_to_hex_string(color):
    r = color >> 16 & 255
    g = color >> 8 & 255
    b = color & 255
    return '#%02x%02x%02x' % (r, g, b)


def rgb_hex_color_to_color(rgb_hex):
    rgb_hex = rgb_hex.replace("#","")
    color_tuple = struct.unpack('BBB', rgb_hex.decode('hex'))
    return Color(color_tuple[0], color_tuple[1], color_tuple[2])


def led_not_configured_error():
    """
    Error handler when the specified pin has not been configured for use with app
    :return: json error message with status code of 400
    """
    return jsonify({
        "Error": {
            "Message": "The led is not configured to be set"
        }
    }), 400


def invalid_data_error():
    """
    Error handler when an invalid page was requested
    :return: json error message with status code 404
    """
    return jsonify({
        "Error": {
            "Message": "Invalid data",
        }
    }), 400


def led_error(e):
    """
    Error handler when something went wrong setting the led
    :param e: The exception
    :return: json error message with status code 500
    """
    return jsonify({
        "Error": {
            "Message": str(e)
        }
    }), 500


@api.errorhandler(404)
def page_not_found():
    """
    Error handler when an invalid page was requested
    :return: json error message with status code 404
    """
    return jsonify({
        "Error": {
            "Message": "Page not found",
        }
    }), 404


@api.errorhandler(400)
def server_error():
    """
    Error handler for any general internal error
    :return: json error message and status code 500
    """
    return jsonify({
        "Error": {
            "Message": "Internal error occurred"
        }
    }), 500


@api.route('/<int:id>/', methods=['GET'])
def get_led(id):
    """
    Returns info about an led
    :param id: (int) the led  to get info about
    :return: json string of info or error
    """
    if id > current_app.config["LEDS"].numPixels() - 1 or id < 0:
        return led_not_configured_error()
    return jsonify({
        "led": {
            "id": id,
            "color": raw_color_to_hex_string(current_app.config['LEDS'].getPixelColor(id))
        }
    })


@api.route('/', methods=['GET'])
def get_leds():
    """
    Returns info about leds
    :return: json string of the configured outputs
    """
    leds = []
    for i in range(current_app.config['LEDS'].numPixels()):
        leds.append({
            "id": i,
            "color": raw_color_to_hex_string(current_app.config['LEDS'].getPixelColor(i))
        })
    return jsonify({"leds": leds})


@api.route('/<int:id>', methods=['PUT'])
def update_led(id):
    """
    Sets the specified led color
    :param id: (int) the led to set
    :return: json message showing the status of the led or error message
    """
    if id > current_app.config["LEDS"].numPixels()-1 or id < 0:
        return led_not_configured_error()
    try:
        data = request.get_json()
        if "led" in data and "color" in data["led"]:
            current_app.config['LEDS'].setPixelColor(id, rgb_hex_color_to_color(data["led"]["color"]))
            current_app.config['LEDS'].show()
        else:
            return invalid_data_error()
    except Exception as e:
        return led_error(e)
    return jsonify({
        "led": {
            "id": id,
            "color": raw_color_to_hex_string(current_app.config['LEDS'].getPixelColor(id))
        }
})
