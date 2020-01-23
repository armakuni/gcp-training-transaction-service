import logging

from transaction_service.app.models.transaction import Transaction


class TransferService:
    def __init__(self, transaction_repository,
                 event_publisher, accounts_client):
        self.transaction_repository = transaction_repository
        self.event_publisher = event_publisher
        self.accounts_client = accounts_client

    def operate(self, operation, amount, account_number):
        self._validate_account(account_number)
        balance = self._calculate_balance(account_number, amount, operation)
        self._store_transaction(account_number, amount, balance, operation)
        self._publish_balance(account_number, balance)

    def _validate_account(self, account_number):
        logging.info('Validating account')
        self.accounts_client.validate_account(account_number)

    def _calculate_balance(self, account_number, amount, operation):
        balance_amount = self._get_current_balance(account_number)
        if operation == 'credit':
            new_balance = balance_amount + amount
        else:
            new_balance = balance_amount - amount
        return new_balance

    def _store_transaction(self,
                           account_number,
                           amount,
                           new_balance,
                           operation):
        logging.info('Saving transaction')
        transaction = Transaction(account_number=account_number,
                                  amount=amount,
                                  transaction_type=operation,
                                  balance=new_balance)
        logging.info('Transaction to save - ' + f'transaction : {transaction}')
        self.transaction_repository.store(transaction)

    def _publish_balance(self, account_number, new_balance):
        logging.info('Publishing the balance')
        message = dict(accountNumber=account_number,
                       clearedBalance=new_balance)
        self.event_publisher.send_message(message)

    def _get_current_balance(self, account_number):
        logging.info('Getting account balance')

        logging.info('Getting latest transaction')
        transaction = self.transaction_repository \
            .get_latest_transaction(account_number)

        logging.info(f'balance transaction : {transaction} ')

        if transaction is None:
            return 0

        return transaction.balance
