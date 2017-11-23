# -*- coding: UTF-8 -*-
from flask import Blueprint, jsonify
from flask import current_app
import RPi.GPIO as GPIO

api = Blueprint('api', __name__)


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


def gpio_error(e):
    """
    Error handler when something went wrong setting the GPIO
    :param e: The exception
    :return: json error message with status code 500
    """
    return jsonify({
        "Error": {
            "Message": e.message
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


@api.errorhandler(500)
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
    if id not in current_app.config['OUTPUTS']:
        return output_not_configured_error()
    return jsonify({
        "id": id,
        "status": GPIO.input(current_app.config['OUTPUTS'][id])
    })


@api.route('/', methods=['GET'])
def get_outputs():
    """
    Returns info about outputs
    :return: json string of the configured outputs
    """
    outputs = []
    for id in current_app.config['OUTPUTS']:
        outputs.append({
            "id": id,
            "status": GPIO.input(current_app.config['OUTPUTS'][id])
        })
    return jsonify(outputs)


@api.route('/<int:id>/on', methods=['POST'])
def set_output_on(id):
    """
    Sets the specified output to be on
    :param id: (int) the output to set
    :return: json message showing the status of the output or error message
    """
    if id not in current_app.config['OUTPUTS']:
        return output_not_configured_error()
    try:
        GPIO.output(current_app.config['OUTPUTS'][id], GPIO.HIGH)
    except Exception as e:
        return gpio_error(e.str())
    return jsonify({
        "id": id,
        "status": GPIO.input(current_app.config['OUTPUTS'][id])
    })


@api.route('/<int:id>/off', methods=['POST'])
def set_output_off(id):
    """
    Sets the specified output to be off
    :param id: (int) the output to change
    :return: json message showing the status of the output or error message
    """
    if id not in current_app.config['OUTPUTS']:
        return output_not_configured_error()
    try:
        GPIO.output(current_app.config['OUTPUTS'][id], GPIO.LOW)
    except Exception as e:
        return gpio_error(e.str())
    return jsonify({
        "id": id,
        "status": GPIO.input(current_app.config['OUTPUTS'][id])
    })