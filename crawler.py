from bs4 import BeautifulSoup
import urllib
import requests
import collections
import sys
import time
import re
import os

def crawl_dblp(professor):
    
    name = professor.strip("\n").split(" ")
    profname = ""
    for i in range(len(name)-1):
        profname += name[i]+"$"
    profname += name[-1]
    
    url = 'http://dblp.org/search/publ/api?q=' + profname + '&format=xml'
    path = os.getcwd() + "/" + professor +"_dblp.txt"
    save = urllib.request.urlretrieve(url, path)


def crawl_arxiv(professor):
    try:
        name = professor.strip("\n").split(" ")
        profname = ""
        for i in range(len(name)-1):
            profname += "all:" + name[i]+"+AND+"
        profname += "all:" + name[-1]

        url = 'http://export.arxiv.org/api/query?search_query=' + profname + '&start=0&max_results=50'
        #path = os.getcwd() + "/" + professor +"_arxiv.txt"
        #save = urllib.request.urlretrieve(url, path)
        xml  = urllib.request.urlopen(url)
        soup = BeautifulSoup(xml.read(), "html.parser")
        titles = soup.find_all('title')
        summaries = soup.find_all('summary')
        dest_url = "papers/"+professor
        with open(dest_url, "w") as f:
            for i in range(1, len(titles)):
                f.write(titles[i].text)
                f.write("\n")
                f.write("\n")
                f.write(summaries[i-1].text)
                f.write("\n")
                f.write("\n")
    except:
        pass


def crawl_scienceDirect(professor):
    name = professor.strip("\n").split(" ")
    profname = ""
    for i in range(len(name)-1):
        profname += name[i]+"+"
    profname += name[-1]

    url = 'http://api.elsevier.com/content/search/scidir?query=KEY%28' + profname + '%29'
    path = os.getcwd() + "/" + professor +"_scienceDirect.txt"
    save = urllib.request.urlretrieve(url, path)

prof_name_list = os.listdir("profs")
if not os.path.exists("papers"):
    os.makedirs("papers")

for prof_name in prof_name_list:
    crawl_arxiv(prof_name)
    time.sleep(0.1)


