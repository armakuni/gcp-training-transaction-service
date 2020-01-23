from transaction_service.app import app
from transaction_service.app.config import test_config
from transaction_service.app.service.transfer_service import TransferService
from transaction_service.mocks.mock_accounts_client import MockAccountsClient
from transaction_service.mocks.mock_event_publisher import MockPubSubClient
from transaction_service.mocks.mock_transaction_repository import \
    MockTransactionRepository


def before_scenario(context, scenario):
    context.transaction_repository = MockTransactionRepository()
    context.publish_msg = MockPubSubClient()
    context.accounts_client = MockAccountsClient()
    context.web_client = app.create(
        config=test_config,
        transfer_service=TransferService(
            transaction_repository=context.transaction_repository,
            event_publisher=context.publish_msg,
            accounts_client=context.accounts_client
        )
    ).test_client()
