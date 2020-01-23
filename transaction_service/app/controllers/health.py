import logging

from flask import Blueprint, jsonify

health = Blueprint('health', __name__, url_prefix='/transactions')


@health.route('health')
def healthcheck():
    logging.info('Healcheck call')
    return jsonify(message='OK')
