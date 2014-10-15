import requests
from bs4 import BeautifulSoup
import re
import datetime

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
    
    for link in soup.find_all(href=re.compile('/olbsys/bbtolbext/accntHist/+')):
        divstrings = link.div.get_text().strip().split()
        account = {}
        account['url'] = link.get('href')
        account['type'] = divstrings[0]
        account['lastno'] = divstrings[1]
        account['amount'] = divstrings[2]
        accounts.append(account)

    print('You have ' + str(len(accounts)) + ' account options.\n')
    for index,account in enumerate(accounts):
        print('Option [' + str(index) + '] is a ' + account['type'] + ' account ending in '\
              + account['lastno'] + ' containing $' + account['amount'])

    inputaccount = raw_input('Choose an account: ')
    account_request = bank_session.get(_base_url + accounts[int(inputaccount)]['url'])
    return (accounts, account_request.text)

def parse(account_page):
    account_soup = BeautifulSoup(account_page)

    
