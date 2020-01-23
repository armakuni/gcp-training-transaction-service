import base64
import json
from http import HTTPStatus

import pytest

from transaction_service.app.exceptions.transaction_service_exceptions import \
    AccountNotFoundException


@pytest.fixture
def request_json():
    return dict(
        id='16fd2706-8baf-433b-82eb-8c7fada847da',
        accountNumber='12345678',
        amount=15,
        operation='debit',
        status='accepted',
        created='2019-01-13T14:14:29Z'
    )


def pub_sub_request(request):
    json_request = json.dumps(request).encode('utf-8')
    encoded = base64.b64encode(json_request).decode('utf-8')
    return dict(message=dict(data=encoded, ignored="ignore me"),
                ignored="ignore me")


def test_post_transactions_returns_bad_request_when_no_body(web_client):
    response = web_client.post('/transactions')
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json['message'] == \
           "Invalid PubSub payload: None should be instance of 'dict'"  # noqa E501


def test_post_transactions_returns_bad_request_when_string_body(web_client):
    response = web_client.post('/transactions', json='string body')
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json['message'] == \
           "Invalid PubSub payload: 'string body' should be instance of 'dict'"  # noqa E501


def test_post_transactions_returns_bad_request_when_number_body(web_client):
    response = web_client.post('/transactions', json=45558)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json['message'] == \
           "Invalid PubSub payload: 45558 should be instance of 'dict'"  # noqa E501


def test_post_transactions_returns_bad_request_message_has_no_data(web_client):
    response = web_client.post('/transactions', json=dict(message=dict()))
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json['message'] == \
           "Invalid PubSub payload: Key 'message' error:\nMissing key: 'data'"  # noqa E501


def test_post_transactions_returns_bad_request_when_id_is_invalid(
        web_client, request_json):
    request_json['id'] = 'short'
    response = web_client.post('/transactions',
                               json=pub_sub_request(request_json))
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_post_transactions_returns_bad_request_when_account_number_is_invalid(
        web_client, request_json):
    request_json['accountNumber'] = '1234'
    response = web_client.post('/transactions',
                               json=pub_sub_request(request_json))
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_post_transactions_returns_bad_request_when_status_is_invalid(
        web_client, request_json):
    request_json['status'] = 'hello'
    response = web_client.post('/transactions',
                               json=pub_sub_request(request_json))
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_post_transactions_returns_bad_request_when_amount_is_invalid(
        web_client, request_json):
    request_json['amount'] = 14.5
    response = web_client.post('/transactions',
                               json=pub_sub_request(request_json))
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_post_transactions_returns_bad_request_when_amount_is_negative(
        web_client, request_json):
    request_json['amount'] = -1
    response = web_client.post('/transactions',
                               json=pub_sub_request(request_json))
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_post_transactions_returns_bad_request_when_operation_is_invalid(
        web_client, request_json):
    request_json['operation'] = 'hello'
    response = web_client.post('/transactions',
                               json=pub_sub_request(request_json))
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_post_transactions_returns_bad_request_when_account_is_invalid(
        web_client, request_json, transfer_service):
    transfer_service.operate.side_effect = AccountNotFoundException()
    response = web_client.post('/transactions',
                               json=pub_sub_request(request_json))
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_post_transactions_returns_ok_on_success(
        web_client, transfer_service, request_json):
    response = web_client.post('/transactions',
                               json=pub_sub_request(request_json))
    assert response.status_code == HTTPStatus.OK
    assert response.json[
               'message'] == 'Successfully processed the transaction.'  # noqa E501


def test_post_transactions_calls_operate_with_debit_transfer_details(
        web_client, transfer_service, request_json):
    request_json['operation'] = 'debit'
    web_client.post('/transactions', json=pub_sub_request(request_json))
    transfer_service.operate.assert_called_with(account_number='12345678',
                                                amount=15,
                                                operation='debit')


def test_post_transactions_calls_operate_with_credit_transfer_details(
        web_client, transfer_service, request_json):
    request_json['operation'] = 'credit'
    web_client.post('/transactions', json=pub_sub_request(request_json))
    transfer_service.operate.assert_called_with(account_number='12345678',
                                                amount=15,
                                                operation='credit')
