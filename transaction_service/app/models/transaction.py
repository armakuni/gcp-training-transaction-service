from datetime import datetime


class Transaction:
    def __init__(self, account_number, amount, transaction_type, balance):
        self.account_number = account_number
        self.amount = amount
        self.transaction_type = transaction_type
        self.timestamp = datetime.timestamp(datetime.now())
        self.balance = balance

    @staticmethod
    def from_dict(source):
        # [START_EXCLUDE]
        transaction = Transaction(
            source[u'account_number'], source[u'amount'],
            source[u'transaction_type'], source[u'balance'])
        transaction.timestamp = source[u'timestamp']
        return transaction
        # [END_EXCLUDE]

    def to_dict(self):
        # [START_EXCLUDE]
        dest = {
            u'account_number': self.account_number,
            u'amount': self.amount,
            u'transaction_type': self.transaction_type,
            u'timestamp': self.timestamp,
            u'balance': self.balance
        }
        return dest
        # [END_EXCLUDE]

    def __repr__(self):
        return (
            f'Transaction('
            f'account_number={self.account_number}, '
            f'amount={self.amount}, '
            f'transaction_type={self.transaction_type}, '
            f'timestamp={self.timestamp}, '
            f'balance={self.balance}'
            f')'
        )
