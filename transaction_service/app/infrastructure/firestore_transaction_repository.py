import logging

from google.cloud import firestore

from transaction_service.app.models.transaction import Transaction


class FireStoreTransactionRepository:
    def __init__(self, transaction_collection):
        db = firestore.Client()
        self.transaction_repo = db.collection(transaction_collection)

    def store(self, transaction):
        doc_ref = self.transaction_repo.document()
        doc_ref.set(transaction.to_dict())

    def get_latest_transaction(self, account_number):
        act_latest_transactions = self.transaction_repo \
            .where(u'account_number', u'==', account_number) \
            .order_by(u'timestamp',
                      direction=firestore.Query.DESCENDING) \
            .limit(1) \
            .stream()

        for doc in act_latest_transactions:
            logging.info(
                f'Retrieving latest transaction - '
                f'This is data : {doc.id} => {doc.to_dict()}'
            )
            return Transaction.from_dict(doc.to_dict())
