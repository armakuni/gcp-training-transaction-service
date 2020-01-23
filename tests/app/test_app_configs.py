from flask import Flask

from transaction_service.app import config


def test_default_config():
    app = Flask(__name__)
    app.config.from_object(config.config)
    assert app.config['SWAGGER_URL']
    assert app.config['SWAGGER_FILE_PATH']
    assert app.config['APP_NAME']
    assert app.config['ENV'] == 'development'


def test_test_config():
    app = Flask(__name__)
    app.config.from_object(config.test_config)
    assert app.config['TESTING']
    assert app.config['TESTING'] == 'true'
