import requests
from bs4 import BeautifulSoup

username = raw_input('Enter your username: ')
print username
payload = {'UserName': username, 'input': 'Go'} 
r = requests.post("https://online.bbt.com/auth/pwd.tb", data = payload)

print (r.text)

