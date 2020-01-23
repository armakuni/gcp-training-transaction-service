class MockTransactionRepository:
    def __init__(self, config_prefix='FIRESTORE_TRANSACTION_COLLECTION'):
        self._store = []
        self.config_prefix = config_prefix

    def store(self, transaction):
        self._store.append(transaction)

    def get_latest_transaction(self, account_number):
        sorted_transactions = sorted(
            self._store,
            key=lambda transaction: transaction.timestamp,
            reverse=True
        )

        if len(sorted_transactions) == 0:
            return None

        return sorted_transactions[0]
