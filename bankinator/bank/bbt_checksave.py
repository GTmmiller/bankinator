import requests
from bs4 import BeautifulSoup
import re
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
                           'UserName': username, 'inq': 'O', 'Password': password}

        auth_request = self._bank_session.post(self._base_url + self._auth_url, data=request_payload)
        return auth_request.text

    def navigate(self, homepage):
        home_soup = BeautifulSoup(homepage)
        accounts = []
    
        for link in home_soup.find_all(href=re.compile('/olbsys/bbtolbext/accntHist/+')):
            div_strings = link.div.get_text().strip().split()
            account = {
                'url': link.get('href'),
                'type': div_strings[0],
                'lastno': div_strings[1],
                'amount': div_strings[2]
            }
            accounts.append(account)

        print('\nYou have ' + str(len(accounts)) + ' account options.\n')
        for index, account in enumerate(accounts):
            print('Option [' + str(index) + '] is a ' + account['type'] + ' account ending in '
                  + account['lastno'] + ' containing $' + account['amount'])

        input_account = raw_input('\nChoose an account: ')
        check_save_table = self._bank_session.get(self._base_url + accounts[int(input_account)]['url'])
        return accounts[int(input_account)], check_save_table.text

    def parse(self, account, account_text):
        account_soup = BeautifulSoup(account_text)
        account_headers = []
        account_transactions = []

        for header in account_soup.table.thead.tr.find_all('th'):
            account_headers.append(header.get_text())

        account_transactions.append(account_headers)

        for row in account_soup.table.tbody.find_all('tr'):
            transaction_row = [row.th.get_text()]
            for table_data in row.find_all('td'):
                transaction_row.append(table_data.get_text())
            account_transactions.append(transaction_row)

        return account, account_transactions
