import sys
import urllib2
import re
import string
from bs4 import BeautifulSoup
import random
import requests

# # URL to scrape from
# web_link = "https://www.jamiiforums.com/threads/teach-individuals-and-not-the-class.1202358/"

# http://willdrevo.com/using-a-proxy-with-a-randomized-user-agent-in-python-requests/
# page = urllib2.urlopen(web_link)
# print page

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

# load the user agents, in random order
user_agents = LoadUserAgents(uafile="user_agents.txt")

proxy = {"http": "http://<username>:<p3ssw0rd>@10.10.1.10:3128"}
url = 'http://api.openweathermap.org/data/2.5/weather'
params = {"q" : "London,uk"}

# load user agents and set headers
uas = LoadUserAgents(uafile="user_agents.txt")
ua = random.choice(uas)  # select a random user agent
headers = {
    "Connection" : "close",  # another way to cover tracks
    "User-Agent" : ua
    }

# make the request
r = requests.get(url, proxies=proxy,
    params=params, headers=headers)

response = r.json
print response
