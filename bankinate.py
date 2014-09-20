import getpass
import requests
import re
import datetime
from bs4 import BeautifulSoup

# Constants

# Username/Password Input
bank_session = requests.Session()
username = raw_input('Enter your username: ')
password = getpass.getpass('Enter your password: ')

# Parameters for Post
request_payload = {'BrowserDetective': 'General Inquiry',
                   'var_field': "",
                   'UserName': username, 'inq': 'O', 'Password': password}

# Login
r = requests.post("https://online.bbt.com/auth/pwd.tb", data=request_payload)
login_cookies = r.cookies
soup = BeautifulSoup(r.text)
# f = open('stuff.html', 'w')
# f.write(r.text)

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

r = bank_session.get("https://online.bbt.com" + accounts[int(inputaccount)]['url'])

today = datetime.date.today()

#f = open('chart.html', 'w')
#f.write(r.text)
soup = BeautifulSoup(r.text)
csv = ''
fout = open(str(today.year) + '_' + str(today.month) + '_' + str(today.day) + \
            '_' + account['type'] + account['lastno'] + '_transactions.csv', 'w')

for row in soup.find('tbody').find_all('tr'):
    for tag in row.contents:
        if tag == u'\n' or tag.get_text().strip() == u'':
            continue
        csv += '"' + " ".join(tag.get_text().strip().split()) + '"' + ','
    csv += '\n'
fout.write(csv)
