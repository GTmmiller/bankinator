import getpass
import requests
import re
from bs4 import BeautifulSoup

# Constants

# Username/Password Input
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

r = requests.get("https://online.bbt.com" + accounts[int(inputaccount)]['url'],\
                 cookies = login_cookies)
f = open('chart.html', 'w')
f.write(r.text)
