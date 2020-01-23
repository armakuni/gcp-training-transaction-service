from flask import Flask
from flask_cors import CORS

from transaction_service.app.controllers.health import health
from transaction_service.app.controllers.swagger import setup_swagger
from transaction_service.app.controllers.transaction import transaction


def create(config, transfer_service):
    app = Flask(__name__)
    app.config.from_object(config)
    CORS(app)
    app.transfer_service = transfer_service
    register_blueprints(app)

    app.register_blueprint(setup_swagger(), url_prefix=config.SWAGGER_URL)
    return app


def register_blueprints(app):
    """Register blueprints with the Flask application."""
    app.register_blueprint(health)
    app.register_blueprint(transaction)
