from unittest.mock import Mock

import pytest

from transaction_service.app import config
from transaction_service.app.app import create


@pytest.fixture
def transaction_repository():
    return Mock()


@pytest.fixture
def event_publisher():
    return Mock()


@pytest.fixture
def accounts_client():
    return Mock()


@pytest.fixture
def transfer_service():
    return Mock()


@pytest.fixture
def app(transaction_repository,
        event_publisher,
        accounts_client,
        transfer_service):

    app = create(config.config, transfer_service=transfer_service)
    return app


@pytest.fixture
def web_client(app):
    return app.test_client()
