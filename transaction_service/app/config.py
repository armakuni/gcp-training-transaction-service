# -*- coding: utf-8 -*-
"""Application configuration."""
from os import environ


class config(object):
    """Base configuration."""
    # SWAGGER
    SWAGGER_URL = environ.get('SWAGGER_URL') or '/docs'
    SWAGGER_FILE_PATH = environ.get(
        'SWAGGER_FILE_PATH') or '/../../../swagger.yml'
    # APPLICATION
    APP_NAME = environ.get('APP_NAME') or 'transaction Service App'
    PORT = environ.get('PORT') or '5002'
    TRANSACTION_NAMESPACE = environ.get(
        'TRANSACTION_NAMESPACE') or 'transactions'
    ENV = environ.get('ENV') or 'development'
    ACCOUNTS_URL = environ.get(
        'ACCOUNTS_SERVICE_URL', default='http://localhost:5001/accounts/')
    BALANCE_TOPIC_ID = environ.get('BALANCE_TOPIC_ID', 'balance')


class test_config():
    """Testing configuration."""
    TESTING = 'true'
    ENV = 'testing'
    # SWAGGER
    SWAGGER_URL = environ.get('SWAGGER_URL') or '/docs'
    SWAGGER_FILE_PATH = environ.get(
        'SWAGGER_FILE_PATH') or '/../../../swagger.yml'

    @classmethod
    def init_app(cls, app):
        print('THIS APP IS IN DEBUG MODE. \
                YOU SHOULD NOT SEE THIS IN PRODUCTION.')
