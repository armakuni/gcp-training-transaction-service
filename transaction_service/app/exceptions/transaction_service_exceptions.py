class AccountNotFoundException(Exception):
    def __init__(self, message='Account not found'):
        self.message = message


class SaveTransactionException(Exception):
    def __init__(self, message='Error accour while saving the transaction'):
        self.message = message


class PublishingError(Exception):
    def __init__(self, message='Error publishing exception'):
        self.message = message
