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
    path = os.getcwd() + "/Evaluation_data/" + professor +"_dblp.txt"
    save = urllib.request.urlretrieve(url, path)

    file = open(path,"r")
    content = file.read()
    num_paper = content.count("<title>")
    return num_paper

def rank(univerity, query):
    file = open(os.getcwd() + "/universities/"+ univerity+" .txt","r")
    prof = file.readline().strip("\n")
    professor_query = [] 
    
    while prof:
        professor_query.append([prof,prof+" "+query])
        prof = file.readline()
    
    professor_rankscore = [[crawl_dblp(x[1]),x[0]] for x in professor_query]

    sorted(professor_rankscore, reverse = True)
    return professor_rankscore
    

    
    
    
    

testcase = open("Testcase.txt","r")
line = testcase.readline()

while line:
    university, query = line.strip("\n").split(", ")
    ranking = rank(university, query)
    print(ranking[:10])
    line = testcase.readline()
