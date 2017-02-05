from flask import Blueprint, jsonify
from flask import current_app
import RPi.GPIO as GPIO

api = Blueprint('api', __name__)


def output_not_configured_error():
    return jsonify({
        "Error": {
            "Message": "The output is not configured to be set by the app"
        }
    })


def gpio_error(e):
    return jsonify({
        "Error": {
            "Message": e.message
        }
    })


@api.route('/<int:id>/', methods=['GET'])
def get_output(id):
    if id not in current_app.config['OUTPUTS']:
        return output_not_configured_error()
    return jsonify({
        "id": id,
        "status": GPIO.input(current_app.config['OUTPUTS'][id])
    })


@api.route('/<int:id>/on', methods=['POST'])
def set_output_on(id):
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