import getpass
import requests
import re
from datetime import datetime
from bs4 import BeautifulSoup
import calendar
from string import Template

# Constants

# Username/Password Input
bank_session = requests.Session()
username = raw_input('Enter your username: ')
password = getpass.getpass('Enter your password: ')

# Parameters for Post
request_payload = {'BrowserDetective': 'General Inquiry',
                   'var_field': "", 'UserName': username, 'inq': 'O',
                   'Password': password}

# Login
r = requests.post("https://online.bbt.com/auth/pwd.tb", data=request_payload)
login_cookies = r.cookies
soup = BeautifulSoup(r.text)
#f = open('stuff.html', 'w')
#f.write(r.text)

accounts = []

# parse bank accounts
for link in soup.find_all(href=re.compile('/olbsys/bbtolbext/accntHist/+')):
    divstrings = link.div.get_text().strip().split()
    account = {}
    account['url'] = link.get('href')
    account['type'] = divstrings[0]
    account['lastno'] = divstrings[1]
    account['amount'] = divstrings[2]
    accounts.append(account)

# parse credit card accounts
for link in soup.find_all(href=re.compile('/olbsys/bbtolbext/bankcards/+')) :
    if link.div != None:
        typeAndLastNo = link.div.contents[0].strip().rsplit(None, 1)
        account = {}
        account['url'] = link.get('href')
        account['type'] = typeAndLastNo[0]
        account['lastno'] = typeAndLastNo[1]
        account['amount'] = link.div.h3.get_text().strip() + ' ' + link.div.span.get_text()
        accounts.append(account)

print('You have ' + str(len(accounts)) + ' account options.\n')

for index,account in enumerate(accounts):
    print('Option [' + str(index) + '] is a ' + account['type'] + ' account ending in '\
          + account['lastno'] + ' with a balance of $' + account['amount'])

inputaccount = raw_input('Choose an account: ')

account_params = {'action': 'managePostedTransactions',
                  'action': 'managePostedTransactions',
                  'flag': '3D',
                  'rand': str(calendar.timegm(datetime.utcnow().utctimetuple()))}
# account_request = Template('https://online.bbt.com/olbsys/bbtolbext/bankcards/manageDetails?action=managePostedTransactions&action=managePostedTransactions&flag=3D&rand=0')
# r = bank_session.get("https://online.bbt.com/olbsys/bbtolbext/bankcards/manageDetails",
#                     params = account_params)
 
r = bank_session.get("https://online.bbt.com" + accounts[int(inputaccount)]['url'])
print r.text

f = open('chart.html', 'w')
f.write(r.text)
f.close()

r = bank_session.get('https://online.bbt.com/olbsys/bbtolbext/bankcards/manageDetails?action=managePostedTransactions&action=managePostedTransactions&flag=3D&rand=0')
print r.text

print r.json()
csv = ''

fout = open('chart.html', 'r')
csvfile = open('cc_csvs.csv', 'w')
soup = BeautifulSoup(fout.read())
for row in soup.find('tbody').find_all('tr'):
    csv += '"' + unicode(row.th.get_text()) + '"' + ','
    for td in row.find_all('td'):
        td_string = unicode(' '.join(td.get_text().strip().split()))
        if(td_string != u''):
            csv += '"' + td_string + '"' + ','
    csv += '\n'

print csv

csvfile.write(csv)

'''
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
'''
