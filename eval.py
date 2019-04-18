from bs4 import BeautifulSoup
import urllib
import requests
import collections
import sys
import time
import re
import os
from nltk.corpus import stopwords

def crawl_dblp(professor):
    name = professor.replace("\n","").split(" ")
    profname = ""
    for i in range(len(name)-1):
        profname += name[i]+"$"
    profname += name[-1]
    
    url = 'http://dblp.org/search/publ/api?q=' + profname + '&format=xml'
    path = os.getcwd() + "/Evaluation_data/" + professor +"_dblp.txt"
    save = urllib.request.urlretrieve(url, path)

    file = open(path,"r")
    content = file.read()
    num_paper = content.count("<title>")

    return num_paper

def rank(univerity, query):
    # remove stop words, reform query
    stop_words = stopwords.words('english')
    query_word = query.replace("\n","").split(" ")
    query_word = [word for word in query_word if word not in stop_words]

    tmp = ""
    for i in range(len(query_word)-1):
        tmp += query_word[i]+" "
    tmp += query_word[-1]
    query = tmp

    # readin professors name
    uni_name = ""
    for x in univerity.split(" "):
        uni_name += "\ "+ x
    file = open(os.getcwd() + "/universities/"+ univerity+".txt","r")
    prof = file.readline().strip("\n")
    professor_query = [] 
    
    # search query = prof name + reformed query 
    while prof:
        professor_query.append([prof,prof+" "+query])
        prof = file.readline()
    
    # get rank results
    professor_rankscore = [[crawl_dblp(x[1]),x[0]] for x in professor_query]

    professor_rankscore = sorted(professor_rankscore, reverse = True)
    return professor_rankscore
    

testcase = open("Testcase.txt","r")
line = testcase.readline()

while line:
    university, query = line.strip("\n").split(", ")
    ranking = rank(university, query)
    print(ranking[:10])
    line = testcase.readline()
