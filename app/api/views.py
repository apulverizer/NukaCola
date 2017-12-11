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
    color_tuple = struct.unpack('BBB', rgb_hex.decode('hex'))
    return Color(color_tuple[0], color_tuple[1], color_tuple[2])


def output_not_configured_error():
    """
    Error handler when the specified pin has not been configured for use with app
    :return: json error message with status code of 400
    """
    return jsonify({
        "Error": {
            "Message": "The output is not configured to be set by the app"
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


def gpio_error(e):
    """
    Error handler when something went wrong setting the GPIO
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
def get_output(id):
    """
    Returns info about an output
    :param id: (int) the output to get info about
    :return: json string of info or error
    """
    if id > current_app.config["LEDS"].numPixels() - 1 or id < 0:
        return output_not_configured_error()
    return jsonify({
        "output": {
            "id": id,
            "color": raw_color_to_hex_string(current_app.config['LEDS'].getPixelColor(id))
        }
    })


@api.route('/', methods=['GET'])
def get_outputs():
    """
    Returns info about outputs
    :return: json string of the configured outputs
    """
    outputs = []
    for i in range(current_app.config['LEDS'].numPixels()):
        outputs.append({
            "id": i,
            "color": raw_color_to_hex_string(current_app.config['LEDS'].getPixelColor(i))
        })
    return jsonify({"outputs": outputs})


@api.route('/<int:id>', methods=['PUT'])
def update_output(id):
    """
    Sets the specified output to be on/off
    :param id: (int) the output to set
    :return: json message showing the status of the output or error message
    """
    if id > current_app.config["LEDS"].numPixels()-1 or id < 0:
        return output_not_configured_error()
    try:
        data = request.get_json()
        if "output" in data and "color" in data["output"]:
            current_app.config['LEDS'].setPixelColor(id, rgb_hex_color_to_color(data["output"]["color"]))
        else:
            return invalid_data_error()
    except Exception as e:
        return gpio_error(e)
    return jsonify({
        "output": {
            "id": id,
            "color": current_app.config['LEDS'].getPixelColor(id)
        }
})
