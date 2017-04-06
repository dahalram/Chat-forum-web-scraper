import random
import requests

from bs4 import BeautifulSoup

USER_AGENTS_FILE = 'user_agents.txt'
PROXY_FILE = "list_of_proxies.txt"

# proxy = {"http": "http://username:p3ssw0rd@10.10.1.10:3128"}
proxy = ['96.9.252.114']

def LoadProxy(pfile = PROXY_FILE):
    proxies = []
    st = ""
    with open(pfile, 'r') as pf:
        for p in pf.readlines():
            for ip in p.split(","):
                st = ""
                ip, port = ip.split(":")
                st = st + ip.strip(" \'") + ":" + port.strip(" \'")
                proxies.append(st)
    #print(proxies)
    return proxies

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

url = 'http://api.openweathermap.org/data/2.5/weather'
web_link = "https://www.jamiiforums.com/threads/teach-individuals-and-not-the-class.1202358/"

web_link2 = "https://www.us-proxy.org"

web_link3 = "https://www.jamiiforums.com/"

params = {"q" : "London,uk"}

# main post: "messageinfo primarycontent"
# li that contain ahrefs
ahrefs = [["node forum level_", ""], ["discussionListItem visible", "threads"], 
            ["messageInfo primaryContent", "message"]]

ps = LoadProxy()
# load user agents and set headers
uas = LoadUserAgents()
proxy = random.choice(ps)
ua = random.choice(uas)
headers = {
        "Connection" : "close",  # another way to cover tracks
        "User-Agent" : ua
    }

def findlinks_ahref(url, level):
    ret = []
    r = requests.get(url, proxies=proxy,
        params=params, headers=headers)
    response = BeautifulSoup(r.content, 'lxml')
    secs = response.findAll('li') # use response.findAll('span', {'class': 'items'})
    c_ah = 0
    for i in range(0, len(secs)):
        strg = ""
        cls = secs[i].get('class')
        if cls:
            for st in cls:
                st += " "
                strg += st
            if ahrefs[level][0] in strg:
                a = secs[i].find_all('a')
                hrefs = [link.get('href') for link in a]
                for link in hrefs:
                    if link:
                        if ahrefs[level][1] in link:
                            ret.append(web_link3+link)
    pages = []
    spans = response.findAll('span', {'class': 'items'})
    for span in spans:
        # print(span)
        pass
    return ret

# add proxy and scrape more
# scrape into other pages too
discussions = findlinks_ahref(web_link3, 0)
threads = findlinks_ahref(discussions[0], 1)


postIds = []
userIds = []
timeStamps = []
likes = []
postBody = []
quotedTexts = []
# load proxy
count = 0
five = 0

for thread in threads:
    if five == 5:
        break;
    if count == 40:
        proxy = random.choice(ps)
        ua = random.choice(uas)  # select a random user agent
        count = 0
        five += 1
    count += 1
    headers = {
        "Connection" : "close",  # another way to cover tracks
        "User-Agent" : ua
        }

    r = requests.get(thread, proxies=proxy,
        params=params, headers=headers)
    response = BeautifulSoup(r.content, 'lxml')
    out = open('dump.txt', 'w')
    for text in response.findAll('li'):
        # postid
        postId = text.get('id')
        postIds.append(postId)
        #date time
        datetime = ""
        try:
            datetime = text.find('dl', {'class':'brRightInfo timeStamp'}).text
        except:
            pass
        timeStamps.append(datetime)
        # likes received
        likeText = str(text.find('dl', {'class':'brLikeReceived'}))
        likeText = likeText.split('<span>', 1)[-1]
        likeText = likeText.split('</span>')[0]
        likes.append(likeText)
        # Post body
        try:
            message = text.find('div', {'class':'messageContent'}).text.encode('utf-8')
        except:
            pass
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
        # userID = userid.get("href")
        # userName
        username = str(text.find('h3', {'class':'userText'}))
        username = username.split()
        out.write(message.decode("utf-8"))
        out.write("\n\n\n")
    print(postBody[0])

# //*[@id="post-441629"]

# finds all links to threads in a given page
# level 3: class : messageinfo primaryContent --> the first post
# level 2: discussionlist
# level 1: node forum level






