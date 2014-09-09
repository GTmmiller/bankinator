import getpass
import requests
from bs4 import BeautifulSoup

# Username/Password Input
username = raw_input('Enter your username: ')
password = getpass.getpass('Enter your password: ')

# Parameters for Post
request_payload = {'BrowserDetective': 'General Inquiry',
                   'var_field': "",
                   'UserName': username, 'inq': 'O', 'Password': password}

# 
r = requests.post("https://online.bbt.com/auth/pwd.tb", data=request_payload)

f = open('stuff.html', 'w')
f.write(r.text)

