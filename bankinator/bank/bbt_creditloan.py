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

        print('You have ' + str(len(accounts)) + ' account options.\n')

        for index, account in enumerate(accounts):
            print('Option [' + str(index) + '] is a ' + account['type'] + ' account ending in '\
                  + account['lastno'] + ' with a balance of $' + account['amount'])

        input_account = raw_input('Choose an account: ')

        self._bank_session.get((self._base_url + accounts[int(input_account)]['url']))

        cc_loan_params = {
            'action': 'managePostedTransactions',
            'flag': '3D', 'rand': str(datetime.utcnow()),
            'resetForm': 'true'
        }
        cc_loan_table = self._bank_session.get('https://online.bbt.com/olbsys/bbtolbext/bankcards/manageDetails',
                                               params=cc_loan_params)

        return cc_loan_table.text

    def parse(self, account):
        account_soup = BeautifulSoup(account)
        account_data = []

        for row in account_soup.find('tbody').find_all('tr'):
            data_line = [unicode(row.th.get_text())]
            for td in row.find_all('td'):
                td_string = unicode(' '.join(td.get_text().strip().split()))
                if td_string != u'':
                    data_line.append(td_string)
            account_data.append(data_line)

        return account, account_data
