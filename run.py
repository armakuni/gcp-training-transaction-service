import logging

from transaction_service.app import app
from transaction_service.app.config import config
from transaction_service.app.infrastructure.firestore_transaction_repository \
    import FireStoreTransactionRepository
from transaction_service.app.infrastructure.project_id_fetcher import \
    ProjectIDFetcher
from transaction_service.app.infrastructure.pub_sub_client import PubSubClient
from transaction_service.app.infrastructure.rest_accounts_client import \
    RestAccountsClient
from transaction_service.app.service.transfer_service import TransferService

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    repository = FireStoreTransactionRepository('transactions')
    event_publisher = PubSubClient(
        project_id=ProjectIDFetcher().fetch_project_id(),
        topic_name=config.BALANCE_TOPIC_ID
    )
    accounts_client = RestAccountsClient(config.ACCOUNTS_URL)
    app.create(
        config=config,
        transfer_service=TransferService(
            transaction_repository=repository,
            event_publisher=event_publisher,
            accounts_client=accounts_client
        )
    ).run(host='0.0.0.0', port=int(config.PORT))
