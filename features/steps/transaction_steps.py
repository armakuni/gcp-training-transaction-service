import base64
import json
from datetime import datetime

from behave import given, when, then


def pub_sub_request(request):
    json_request = json.dumps(request).encode('utf-8')
    encoded = base64.b64encode(json_request).decode('utf-8')
    return dict(message=dict(data=encoded))


@given('an account {account_number} has balance {amount:d}')
def create_account(context, account_number, amount):
    context.accounts_client.add(account_number=account_number,
                                account_state='active')

    if amount > 0:
        credit_account(context, account_number, amount)


@given('there is not account with the number {account_number}')
def do_not_create_account(context, account_number):
    pass
    # Intentional no-op


@when('an account {account_number} is credited with {amount:d}')
def credit_account(context, account_number, amount):
    context.web_client.post("/transactions", json=pub_sub_request(dict(
        id='1987b482-5e66-4b7f-bd95-ac76f27ed85d',
        accountNumber=account_number,
        amount=amount,
        operation='credit',
        status='accepted',
        created=datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"))))


@when("an account {account_number} is debited with {amount:d}")
def debit_account(context, account_number, amount):
    context.web_client.post("/transactions", json=pub_sub_request(dict(
        id='1987b482-5e66-4b7f-bd95-ac76f27ed85d',
        accountNumber=account_number,
        amount=amount,
        operation='debit',
        status='accepted',
        created=datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"))))


@then('a account {account_number} should have a balance of {balance:d}')
def assert_account_balance(context, account_number, balance):
    published_event = context.publish_msg.msg_published

    expected_event = dict(accountNumber=account_number, clearedBalance=balance)

    assert published_event == expected_event, \
        f'{repr(published_event)} != {repr(expected_event)}'


@then('a bad transaction should be reported')
def assert_bad_transaction(context):
    published_event = context.publish_msg.msg_published
    assert published_event is None
