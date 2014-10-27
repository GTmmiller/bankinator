import requests
from bs4 import BeautifulSoup
import re

_bank_session = requests.Session()
_base_url = "https://online.bbt.com"
_auth_url = "/auth.pwd.tb"


def authenticate(username, password):
    request_payload = {'BrowserDetective': 'General Inquiry',
                       'var_field': "",
                       'UserName': username, 'inq': 'O', 'Password': password}
    
    auth_request = _bank_session.post(_base_url + _auth_url, data = request_payload)
    return auth_request.text


def navigate(homepage):
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

    print('You have ' + str(len(accounts)) + ' account options.\n')
    for index, account in enumerate(accounts):
        print('Option [' + str(index) + '] is a ' + account['type'] + ' account ending in '\
              + account['lastno'] + ' containing $' + account['amount'])

    input_account = raw_input('Choose an account: ')
    return accounts[int(input_account)]


def parse(account):
    account_request = _bank_session.get(_base_url + account['url'])
    account_soup = BeautifulSoup(account_request.text)
    account_data = []

    for row in account_soup.find('tbody').find_all('tr'):
        data_line = []
        for tag in row.contents:
            if tag == u'\n' or tag.get_text().strip() == u'':
                continue
            else:
                data_line.append(unicode(' '.join(tag.get_text().strip.split())))
        account_data.append(data_line)

    return account, account_data
