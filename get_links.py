import random
import requests
import re
import time

from bs4 import BeautifulSoup

##########################################################################################

####### this portion is for getting links to scrape with ##########################


USER_AGENTS_FILE = 'user_agents.txt'
PROXY_FILE = "list_of_proxies.txt"

# proxy = {"http": "http://username:p3ssw0rd@10.10.1.10:3128"}
proxy = ['96.9.252.114']

http_proxy  = "http://10.10.1.10:3128"
https_proxy = "https://10.10.1.11:1080"
ftp_proxy   = "ftp://10.10.1.10:3128"

tag_class_pairs = {
        "for discussions"                 :     ( 'li' ,    'node forum level', ""),
        "for threads"                    :    ( 'li',    'discussionListItem visible', "threads"),
        "for posts' body"                :    ( 'div',  'messageContent'),
        "for posts' likes"               :   ( 'dl',    'brLikeReceived'),
        "for liked by"                   :   ( 'div',  'publicControl'),
        "for quoted text"                :    ( 'div',  'quote' ),
        "for username"                   :   ('h3', 'userText'),
        "for datetime"                   :   ('dl', 'brRightInfo timeStamp'),
        "for pagenav"                    :   ('div', 'PageNav')
    }

def LoadProxy(pfile = PROXY_FILE):
    proxies = {}
    with open(pfile, 'r') as pf:
        for p in pf.readlines():
            for ip in p.split(","):
                proxies["http"] = "http://" + ip
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

JAMII_URL = "https://www.jamiiforums.com/"

params = {"q" : "London,uk"}
proxy = LoadProxy()
# load user agents and set headers
uas = LoadUserAgents()
# proxy = random.choice(ps)
ua = random.choice(uas)
headers = {
        "Connection" : "close",  # another way to cover tracks
        "User-Agent" : ua
    }

# ahrefs contains div classes that we want to scrape for a given level
ahrefs = [["node forum level_", ""], ["discussionListItem visible", "threads"], 
            ["messageInfo primaryContent", "message"]]
# level 0 is landing page, jammiforum.com
# level 1 is the page of threads
# level 2 is the page of actual posts
def findlinks_ahref(url, level):
    next_level_links = []
    r = requests.get(url, proxies=proxy,
        params=params, headers=headers)
    response = BeautifulSoup(r.content, 'lxml')
    secs = response.findAll('li') # use response.findAll('span', {'class': 'items'})
    if level == 0:
        tag = "for discussions"
    else:
        tag = "for threads"
    secs = response.findAll(tag_class_pairs[tag][0], {'class': re.compile(tag_class_pairs[tag][1])})
    print("Secs: ", secs)
    for sec in secs:
        a = sec.find_all('a')
        hrefs = [link.get('href') for link in a]
        for link in hrefs:
            if link:
                if tag_class_pairs[tag][2] in link:
                    next_level_links.append(JAMII_URL+link)
    
    # returns list with div elements
    other_pages=[]
    pages = response.findAll(tag_class_pairs["for pagenav"][0], {'class':re.compile(tag_class_pairs["for pagenav"][1])}) 
    for page in pages[:len(pages)-1]:
        a_s = page.find_all('a', {'href': re.compile("page-")})
        # get 'forums/great-thinkers.110/page-' portion of the href
        gen = a_s[0].get('href')
        gen = gen[:len(gen)-1]

        # m denotes number of pages available to scrape
        m = max([int(a.text) for a in a_s if a.text])
        for i in range(1, m+1):
            other_pages.append(JAMII_URL+gen+str(i))
    return next_level_links, other_pages

# TO-DO (written on 04/17/2017): 
#   manage formatting of posts in terms of likes received, author, replies ...
#   before doing one big scrape using all discussions except only discussion[0]
#   as well as other_pages

# requirements next iteration:
#   likes received, info about who liked, click to expand

# file with just posts
# file with metadata

##############################################################################

############## scrape using available links and dump into dump.txt ##########

postIds = []
userIds = []
timeStamps = []
likes = []
postBody = []
quotedTexts = []
# load proxy
count = 0
four = 0

out = open('dump.txt', 'a')
link_num = open('link_num.txt', 'a')

discussions, _ = findlinks_ahref(JAMII_URL, 0)
discussions = set(discussions)
print("Discussions: ", discussions)

def scrape(url, headers):
    liked_by_users = []
    r = requests.get(url, proxies=proxy,
            params=params, headers=headers)
    response = BeautifulSoup(r.content, 'lxml')
    out.write(url + ':\n\n')
    print("Scraping currently: ", url[36:])
    for text in response.findAll('li'):
        # print ("Text is: \n\n\n", text)
        message = b''
        # postid
        postId = text.get('id')
        postIds.append(postId)
        # date time
        datetime = ""
        st = ""
        try:
            datetime = text.find(tag_class_pairs["for datetime"][0], {'class':tag_class_pairs["for datetime"][1]}).text
        except:
            pass
        timeStamps.append(datetime)
        # likes received
        likeText = str(text.find(tag_class_pairs["for posts' body"][0], {'class': tag_class_pairs["for posts' body"][1]}))
        likeText = likeText.split('<span>', 1)[-1]
        likeText = likeText.split('</span>')[0]
        likes.append(likeText)
        try:
            names = str(text.find(tag_class_pairs["for liked by"][0], {'class':tag_class_pairs["for liked by"][1]}).find_all('a', {'href':re.compile('posts')}))
            try:
                "href" in names.split(" ")[4]
                href = names.split(" ")[4]
            except:
                href = names.split(" ")[3]
                liked_by_users.extend(JAMII_URL+"/"+href)
            # print('href: ', href)
        except:
            pass
        
        # Post body2
        try:
            message = text.find(tag_class_pairs["for posts' body"][0], {'class':tag_class_pairs["for posts' body"][1]}).text.encode('utf-8')
        except:
            pass
        postBody.append(message)
        # Quoted text
        quotedText = ""
        try:
            quotedText = text.find(tag_class_pairs["for quoted text"][0], {'class':tag_class_pairs["for quoted text"][1]}).text
        except:
            pass
        quotedTexts.append(quotedText)
        # userID
        userid = text.findAll('a')
        # userID = userid.get("href")
        # userName
        username = str(text.find(tag_class_pairs["for username"][0], {'class':tag_class_pairs["for username"][1]}))
        username = username.split()
        out.write("\n")
        st = str(postId) + " , " + str(datetime) +  " , " +message.decode("utf-8")
        out.write(st)
        #c += 1

for diss in discussions:
    threads, other_pages = findlinks_ahref(diss, 1)
    threads = set(threads)
    threads = sorted(threads)
    c = 1
    # inside each thread, th is the actual 
    # check for duplicates
    for th in threads:
        link_num.write(str(c) + " " + th)
        link_num.write('\n\n')
        if four == 4:
            time.sleep(10*random.random())
        if count == 40:
            # proxy = random.choice(ps)
            ua = random.choice(uas)  # select a random user agent
            count = 0
            print("Four value: ", four)
            four += 1
        count += 1
        headers = {
            "Connection" : "close",  # another way to cover tracks
            "User-Agent" : ua
            }
        scrape(th, headers)

# url = "https://www.jamiiforums.com/threads/duru-za-siasa-us-chini-ya-d-j-trump.1187811/"
# scrape(url, {})
out.close()
