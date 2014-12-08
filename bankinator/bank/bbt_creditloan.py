import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
from base_bank import BankBase


class Bank(BankBase):

    def __init__(self):
        BankBase.__init__(self)
        self._bank_session = requests.Session()
        self._base_url = 'https://online.bbt.com'
        self._auth_url = '/auth/pwd.tb'

    def authenticate(self, username, password):
        request_payload = {'BrowserDetective': 'General Inquiry',
                           'var_field': '',
                           'UserName': username, 'inq': 'O',
                           'Password': password}

        auth_request = self._bank_session.post(self._base_url + self._auth_url, data=request_payload)
        return auth_request.text

    def navigate(self, homepage):
        home_soup = BeautifulSoup(homepage)
        accounts = []

        # parse credit card accounts
        for link in home_soup.find_all(href=re.compile('/olbsys/bbtolbext/bankcards/+')):
            if link.div is not None:
                type_and_lastno = link.div.contents[0].strip().rsplit(None, 1)
                account = {
                    'url': link.get('href'),
                    'type': type_and_lastno[0],
                    'lastno': type_and_lastno[1],
                    'amount': link.div.h3.get_text().strip() + ' ' + link.div.span.get_text()
                }
                accounts.append(account)

        print('\nYou have ' + str(len(accounts)) + ' account options.\n')

        for index, account in enumerate(accounts):
            print('Option [' + str(index) + '] is a ' + account['type'] + ' account ending in '\
                  + account['lastno'] + ' with a balance of $' + account['amount'])

        input_account = raw_input('\nChoose an account: ')

        self._bank_session.get((self._base_url + accounts[int(input_account)]['url']))

        cc_loan_params = {
            'action': 'managePostedTransactions',
            'flag': '3D', 'rand': str(datetime.utcnow()),
            'resetForm': 'true'
        }
        cc_loan_table = self._bank_session.get('https://online.bbt.com/olbsys/bbtolbext/bankcards/manageDetails',
                                               params=cc_loan_params)

        return accounts[int(input_account)], cc_loan_table.text

    def parse(self, account, account_text):
        account_soup = BeautifulSoup(account_text)
        account_headers = []
        account_transactions = {}

        # Retain the original order of the headers so the table rows eventually
        # match the columns
        for header in account_soup.table.thead.tr.find_all('th'):
            account_headers.append(header.get_text())
            account_transactions[header.get_text()] = []

        for row in account_soup.table.tbody.find_all('tr'):
            account_transactions[account_headers[0]].append(row.th.get_text())

            for index, table_data in enumerate(row.find_all('td')):
                account_transactions[account_headers[index + 1]].append(''.join(table_data.get_text()).strip().split())

        return account, account_transactions
