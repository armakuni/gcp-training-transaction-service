import logging
import requests

from transaction_service.app.exceptions.transaction_service_exceptions import \
    AccountNotFoundException


class RestAccountsClient:
    def __init__(self, accounts_service_url):
        self.accounts_url = accounts_service_url

    def validate_account(self, account_number):
        logging.info('Requesting information to validate account with number '
                     + account_number)

        resp = requests.get(self.accounts_url + '/accounts/' + account_number)
        if resp.status_code != 200:
            logging.error('Invalid account with number ' + account_number)
            raise AccountNotFoundException()
        logging.info('Valid account with number ' + account_number)
