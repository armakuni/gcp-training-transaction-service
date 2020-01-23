from transaction_service.app.exceptions.transaction_service_exceptions import \
    AccountNotFoundException


class MockAccountsClient:
    def __init__(self):
        self.accounts = []

    def add(self, account_number, account_state):
        self.accounts.append(account_number)

    def validate_account(self, account_number):
        if account_number not in self.accounts:
            raise AccountNotFoundException()
