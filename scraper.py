import sys
import urllib2
import re
import string
from bs4 import BeautifulSoup


## Check this out first https://www.jamiiforums.com/robots.txt
## http://monzool.net/blog/2007/10/15/html-parsing-with-beautiful-soup/


## TODO Use proxy to change the IP address
## Pause for a specific amount of time after a number of iterations

# URL to scrape from
web_link = "https://www.jamiiforums.com/threads/teach-individuals-and-not-the-class.1202358/"

page = urllib2.urlopen(web_link)

# To see the webpage results
# print page.read()
# print page.headers

# Parse the html in the page
parsed_docs = BeautifulSoup(page, "lxml")

# The message content is inside the div with class 'messageContent'

# All the information we need (the texts), is inside this class
# The code below captures all the information (of course with a lot of useless stuffs as well)
# text = parsed_docs.findAll('div', {"class": "messageContent"})
text = parsed_docs.findAll('li')

# check = text.findAll('div', {"class": "messageContent"})

postIds = []
userIds = []
timeStamps = []
likes = []
postBody = []
quotedTexts = []
for text in parsed_docs.findAll('li'):
	# PostID
	postId = text.get('id')
	postIds.append(postIds)

	# Datetime Stamp
	datetime = ""
	try:
		datetime = text.find('dl', {'class':'brRightInfo timeStamp'}).text
	except:
		pass
	timeStamps.append(datetime)

	# Likes Received
	likeText = str(text.find('dl', {'class':'brLikeReceived'}))
	likeText = likeText.split('<span>', 1)[-1]
	likeText = likeText.split('</span>')[0]
	likes.append(likeText)

	# Post body
	message = text.find('div', {'class':'messageContent'}).text.encode('utf-8')
	postBody.append(message)

	# Quoted text
	quotedText = ""
	try:
		quotedText = text.find('div', {'class':'quote'}).text
	except:
		pass

	quotedTexts.append(quotedText)

	# userID
	userid = text.findAll('a')
	userID = userid.get("href")

	# userName
	username = str(text.find('h3', {'class':'userText'}))
	username = username.split()


	# TODO
	# threadId
	# userId 
	# userName
	# quotedPosts 


	print "****************************\n\n"

# print postIds, timeStamps, likes


def getPostId(text):
	for tag in text:
		return tag.get('id')



def getThreadId(text):
	pass

def getUserId(text):
	pass


def getUserName(text):
	pass


def getPostDate(text):
	pass


def getPostTitle(text):
	pass


def getPostBody(text):
	pass


def getQuotedPosts(text):
	pass


def getQuotedTexts(text):
	pass


def getLikedBy(text):
	pass




# print text
# f = open('out.txt', 'w')
# f.write(t2)
# f.close()

