from unittest.mock import patch

import pytest

from transaction_service.app.exceptions.transaction_service_exceptions import \
    AccountNotFoundException
from transaction_service.app.infrastructure.rest_accounts_client import \
    RestAccountsClient


# This method will be used by the mock to replace requests.get
def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if args[0] == 'http://localhost:5001/accounts/12345678':
        return MockResponse(dict(
            accountNumber=12345678,
            accountStatus='active',
            customerId='YvNFAgR3KrYpjHoch4GZ'
        ), 200)
    elif args[0] == 'http://localhost:5001/accounts/11122233':
        return MockResponse(dict(message='Not found'), 404)

    return MockResponse(None, 404)


@patch('requests.get', side_effect=mocked_requests_get)
def test_validate_account_raises_exception_for_invalid_account(request_get):
    with pytest.raises(AccountNotFoundException):
        RestAccountsClient('http://localhost:5001') \
            .validate_account('11113333')


@patch('requests.get', side_effect=mocked_requests_get)
def test_validate_account_does_not_raise_if_account_is_found(request_get):
    RestAccountsClient('http://localhost:5001').validate_account('12345678')
