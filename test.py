import sys
import urllib2
import re
import string
from bs4 import BeautifulSoup

# URL to scrape from
web_link = "https://www.jamiiforums.com/threads/teach-individuals-and-not-the-class.1202358/"

page = urllib2.urlopen(web_link)
print page
