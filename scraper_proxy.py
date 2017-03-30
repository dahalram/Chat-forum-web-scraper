
'''
import urllib.request

from bs4 import BeautifulSoup

# URL to scrape from
web_link = "https://www.jamiiforums.com/threads/teach-individuals-and-not-the-class.1202358/"


## TODO Use proxy to change the IP address
## Pause for a specific amount of time after a number of iterations
proxy = urllib.request.ProxyHandler({'http' : '127.0.0.1'})
opener = urllib.request.build_opener(proxy)
urllib.request.install_opener(opener)
page1 = urllib.request.urlretrieve(web_link)
page2 = urllib.request.urlopen(web_link)

# page = urllib2.urlopen(web_link)
page = urllib.request.urlopen(web_link)

print("Type of page1: ", type(page1))
print("Type of page2: ", type(page1))

# To see the webpage results
# print page.read()
# print page.headers

# Parse the html in the page
parsed_docs = BeautifulSoup(page, "lxml")
parsed_docs1 = BeautifulSoup(page1, "lxml")
parsed_docs2 = BeautifulSoup(page2, "lxml")

print (parsed_docs)

print ('New page \n\n\n\n')

print (parsed_docs1)

print ('New page \n\n\n\n')

print(parsed_docs2)

'''

import random
import requests

USER_AGENTS_FILE = 

proxy = {"http": "http://username:p3ssw0rd@10.10.1.10:3128"}
url = 'http://api.openweathermap.org/data/2.5/weather'
web_link = "https://www.jamiiforums.com/threads/teach-individuals-and-not-the-class.1202358/"
params = {"q" : "London,uk"}

def LoadUserAgents(uafile=USER_AGENTS_FILE):
    """
    uafile : string
        path to text file of user agents, one per line
    """
    uas = []
    with open(uafile, 'rb') as uaf:
        for ua in uaf.readlines():
            if ua:
                uas.append(ua.strip()[1:-1-1])
    random.shuffle(uas)
    return uas



# load user agents and set headers
uas = LoadUserAgents()
ua = random.choice(uas)  # select a random user agent
headers = {
    "Connection" : "close",  # another way to cover tracks
    "User-Agent" : ua
    }

# make the request
r = requests.get(web_link, proxies=proxy,
    params=params, headers=headers)

print (r)
















