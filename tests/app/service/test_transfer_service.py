import pytest

from transaction_service.app.exceptions.transaction_service_exceptions import \
    AccountNotFoundException, SaveTransactionException
from transaction_service.app.models.transaction import Transaction
from transaction_service.app.service.transfer_service import TransferService


@pytest.fixture
def transfer_service(transaction_repository, event_publisher, accounts_client):
    transaction_repository.get_latest_transaction.return_value = None

    return TransferService(transaction_repository,
                           event_publisher,
                           accounts_client)


def test_operate_stores_transaction(transaction_repository, transfer_service):
    transfer_service \
        .operate(operation='credit', account_number='12345678', amount=12)
    transaction_repository.store.assert_called()
    transaction = transaction_repository.store.call_args_list[0][0][0]
    assert transaction.account_number == '12345678'
    assert transaction.amount == 12
    assert transaction.transaction_type == 'credit'
    assert transaction.balance == 12


def test_operate_publishes_balance(event_publisher, transfer_service):
    transfer_service \
        .operate(operation='credit', account_number='12345678', amount=12)

    event_publisher.send_message \
        .assert_called_with(dict(accountNumber='12345678', clearedBalance=12))


def test_operate_verifies_the_account(accounts_client, transfer_service):
    transfer_service \
        .operate(operation='credit', account_number='87654321', amount=42)

    accounts_client.validate_account.assert_called_with('87654321')


def test_operate_does_not_store_transaction_incase_of_invalid_account(
        accounts_client, transaction_repository, transfer_service):
    accounts_client.validate_account.side_effect = AccountNotFoundException()

    with pytest.raises(AccountNotFoundException):
        transfer_service \
            .operate(operation='credit', account_number='1234567', amount=12)

    transaction_repository.store.assert_not_called()


def test_operate_does_not_publish_incase_of_invalid_account(
        accounts_client, event_publisher, transfer_service):
    accounts_client.validate_account.side_effect = AccountNotFoundException()

    with pytest.raises(AccountNotFoundException):
        transfer_service \
            .operate(operation='credit', account_number='1234567', amount=12)

    event_publisher.send_message.assert_not_called()


def test_operate_publish_incase_of_store_failed(
        event_publisher, transaction_repository, transfer_service):
    transaction_repository.store.side_effect = SaveTransactionException()

    with pytest.raises(SaveTransactionException):
        transfer_service \
            .operate(operation='credit', account_number='1234567', amount=12)

    event_publisher.send_message.assert_not_called()


def test_operate_credits_balance(event_publisher,
                                 transaction_repository,
                                 transfer_service):
    account_number = '12341234'
    previous = Transaction(account_number=account_number,
                           amount=10,
                           transaction_type='credit',
                           balance=50)
    transaction_repository.get_latest_transaction.return_value = previous

    transfer_service \
        .operate(operation='credit', account_number=account_number, amount=12)

    transaction_repository.get_latest_transaction \
        .assert_called_with(account_number)

    transaction_repository.store.assert_called()
    transaction = transaction_repository.store.call_args_list[0][0][0]
    assert transaction.balance == 62

    event_publisher.send_message \
        .assert_called_with(dict(accountNumber=account_number,
                                 clearedBalance=62))


def test_operate_debits_balance(event_publisher,
                                transaction_repository,
                                transfer_service):
    account_number = '12341234'
    previous = Transaction(account_number=account_number,
                           amount=10,
                           transaction_type='credit',
                           balance=100)
    transaction_repository.get_latest_transaction.return_value = previous

    transfer_service \
        .operate(operation='debit', account_number=account_number, amount=10)

    transaction_repository.get_latest_transaction \
        .assert_called_with(account_number)

    transaction_repository.store.assert_called()
    transaction = transaction_repository.store.call_args_list[0][0][0]
    assert transaction.balance == 90

    event_publisher.send_message \
        .assert_called_with(dict(accountNumber=account_number,
                                 clearedBalance=90))
