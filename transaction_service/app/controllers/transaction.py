import base64
import json
import logging
from http import HTTPStatus

from dateutil.parser import parse
from flask import Blueprint, jsonify, current_app, request
from schema import Schema, And, SchemaError, Optional

from transaction_service.app.exceptions.transaction_service_exceptions import \
    AccountNotFoundException

transaction = Blueprint('transaction', __name__, url_prefix='/')

PUBSUB_SCHEMA = Schema({
    'message': {'data': str, Optional(str): object},
    Optional(str): object
})

PAYLOAD_SCHEMA = Schema(dict(id=And(str, lambda s: len(s) == 36),
                             accountNumber=And(str, lambda s: len(s) == 8),
                             amount=And(int, lambda n: n > 0),
                             status=lambda s: s in ['accepted'],
                             operation=lambda s: s in ['debit', 'credit'],
                             created=lambda s: parse(s)))


@transaction.route('transactions', methods=['POST'])
def process_transactions():
    transfer_service = current_app.transfer_service
    request_json = request.get_json()

    try:
        PUBSUB_SCHEMA.validate(request_json)
    except SchemaError as e:
        msg = f'Invalid PubSub payload: {str(e)}'
        logging.error('Transaction Error - ' + msg)
        return jsonify(message=msg), 400

    message = request_json['message']

    transaction_data = json.loads(base64.b64decode(message['data'])
                                  .decode('utf-8')
                                  .strip())

    logging.info('Transaction Data: ' + str(transaction_data))

    if not transaction_data:
        msg = 'no Pub/Sub message received'
        logging.error('Transaction Error - ' + msg)
        return jsonify(message=f'Bad Request: {msg}'), 400

    PAYLOAD_SCHEMA.validate(transaction_data)

    transfer_service.operate(
        operation=transaction_data['operation'],
        amount=transaction_data['amount'],
        account_number=transaction_data['accountNumber']
    )

    success_message = 'Successfully processed the transaction.'
    logging.info(success_message)
    return jsonify(message=success_message), HTTPStatus.OK


@transaction.errorhandler(SchemaError)
def schema_error(e):
    logging.warning(f'Schema Error - {str(e)}')
    return jsonify(message=str(e).rstrip('\n')), HTTPStatus.BAD_REQUEST


@transaction.errorhandler(AccountNotFoundException)
def account_not_found(e):
    return jsonify(message=str(e.message)), HTTPStatus.BAD_REQUEST
