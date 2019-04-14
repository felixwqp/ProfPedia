from collections import defaultdict
import math
import sys
import numpy as np

class Paper:
  def Paper(self):
      self.title = ""
      self.date = 0
      self.abstract = ""
      
class Professor:
  def Professor(self):
    self.name = ""
    self.homepage_url = ""
    self.university = ""
    self.field = []
  

prof_to_info_map = {}
prof_to_paperids_map = {}
profs_to_score_map = {}
paperid_to_vector_map = {}
paperid_to_words_of_title = {}
inverted_index = {}
docLen = {}


def getData():
  #fron test;

def preprocesss(doc_str):
  #output: list of tokens
  pass

def inverted_index(doc):
  pass



def construct_vector_space_model(doc_str):
  #output: word_weight_vector
  pass




def get_score_for_paper(query, paperid):
  #output: score for paperid
  paperVector = paperid_to_vector_map[paperid]
  titleSet = paperid_to_words_of_title[paperid]
  query  = preprocesss(query)
  queryLen = float(0)
  queryDict = defaultdict(lambda: 0)

  # recorded the tf and max tf
  maxTf_ = 1
  lenQuery = len(query)
  for i in range(lenQuery):
    word = query[i]
    if(word in titleSet):
      query.append(word)
  # for normalization::
  newQuery = ' '.join(query)
  vecQuery = construct_vector_space_model(newQuery)

  queryVector = np.array(vecQuery)
  paperVector = np.array(paperVector)



  return np.dot(queryVector, paperVector)


def get_score_for_profs(query):
  #output: profs_to_score_map
  pass

def prof_in_constraints(prof_name, university, field)
  pass

def handle_query(query):
  query = ""
  university = ""
  field = ""
  get_score_for_profs(query)
  rankedProfs = list({k: v for k, v in sorted(profs_to_score_map.items(), key=lambda x: x[1], reverse= True)}.items())
  count = 0
  for prof, score in rankedProfs:
    if prof_in_constraints(prof, university, field):
      count += 1
      printProf(prof)
      if count == 10:
        break


def printProf(profName):
  # f = open(profName, 'r')
  print(profName)
  profInfo = prof_to_info_map[profName]
  print(profInfo.home)
  # f.close()

def main():
  getData()
  # inverted_index()
  # construct_vector_space_model()

  query  = ""

  while(query != ""):
    handle_query(query)

  pass

