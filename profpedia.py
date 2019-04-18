# -*- coding: utf-8 -*-
import os, sys
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import string
import math
import operator
  

class Paper():
  def Paper(self):
      self.title = []
      self.date = 0
      self.abstract = []
      
class Professor():
  def Professor(self):
    self.name = ""
    self.homepage_url = ""
    self.university = ""
    self.field = []
  
#name of prof - > prof class?
prof_to_info_map = dict()
#prof -> list of doc_ids
prof_to_paperids_map = dict()
paperid_to_vector_map  = dict()
#id -> set of words
paperid_to_words_of_title = dict()
#term -> df & tf for each doc which is a double dimension dict
#inverted_index doesnt store the title !!! 
inverted_index = dict()
paper_list = []

doc_id = 0
avg_doc_length = 0.0

#read each file from dir "papers" 
def read_doc():
    global doc_id
    global inverted_index
    global prof_to_paperids_map
    global paperid_to_words_of_title
    global prof_to_info_map
    global paper_list
    global avg_doc_length
    
    
    papers_dir = os.listdir('papers_test')

    for i in range(len(papers_dir)):
        each_file = open(os.path.join('papers_test', papers_dir[i]), 'r').read().splitlines()
        j = 0
        prof_name = papers_dir[i]
        temp_prof = Professor()
        temp_prof.name = prof_name
        #TODO:
        #add in other basic info for each prof
        prof_to_info_map[prof_name] = temp_prof
        
        #if none element in professor txt, it should skip the while loop
        while j < len(each_file) :
            currPaper = Paper()
            #title 
            title = preprocesss(each_file[j])
            currPaper.title = title
            '''
            if prof_name not in prof_to_paperids_map:
                prof_to_paperids_map[prof_name] = list()
            prof_to_paperids_map[prof_name].append(doc_id)
            
            doc_id = doc_id + 1
            '''
            #abstract
            abstract = preprocesss(each_file[j+2])
            currPaper.abstract = abstract
            avg_doc_length += len(abstract)
            
            if prof_name not in prof_to_paperids_map:
                prof_to_paperids_map[prof_name] = list()
            prof_to_paperids_map[prof_name].append(doc_id)
            paperid_to_words_of_title[doc_id] = set(title)
            cal_inverted_index(abstract, doc_id, inverted_index)
            doc_id = doc_id + 1

            paper_list.append(currPaper)
            j = j + 4

    avg_doc_length/=len(paper_list) 
                
        #indexDocument(each_doc, doc_weighting, query_weighting, inverted_index)


#pass each doc (title/abstract) and return the list of tokens
#remove stopword  & porter stemming
def preprocesss(doc_str):
  
    ps = PorterStemmer()
    '''
    for i in range(len(doc_str)):
      for punctuation in string.punctuation:
        doc_str[i] = doc_str[i].replace(punctuation, ' ')
    '''
    doc_str = nltk.word_tokenize(doc_str)
    doc_str = [word for word in doc_str if word not in stopwords.words('english') ]
    output_str = []
    for word in doc_str:
        output_str.append(ps.stem(word))
        
    return output_str

#layout of inverted_index  {each_term:{(0:df), (docid:tf)}}
def cal_inverted_index(each_doc,docid,inverted_index):

    for term in each_doc:
        if term in inverted_index:
            if docid in inverted_index[term]:
                inverted_index[term][docid] = inverted_index[term][docid] + 1
            else:
                inverted_index[term][docid] = 1
                #inverted_index[term][0] is doc frequency of each term
                inverted_index[term][0] = inverted_index[term][0] +1
        else:
            inverted_index[term] = dict()
           
            inverted_index[term][0] = 1
            inverted_index[term][docid] = 1


# output: dict of vector weights for 1 doc(paper/query): {term : weight} 
# NOTE: each vector_model only contains the weights of the terms 
# that exist inside each paper.             
def construct_single_vector(doc_tokens, docid):
    output_vector = {}
    uniqueTokens = set(doc_tokens)

    maxFreq = 0
    for token in uniqueTokens: 
        if doc_tokens.count(token) > maxFreq:
            maxFreq = doc_tokens.count(token)

    for token in uniqueTokens: 
        if token in inverted_index:
            tf = (float(inverted_index[token][docid])/float(maxFreq))
            idf = math.log10(float(len(paper_list))/float(inverted_index[token][0]))
            
            # tf-idf weights
            weight_TFIDF = tf * idf
            # BM-25 weights, with tuning factors k1 = 1.2, b = 0,75
            weight_BM = ((tf * (1.2 + 1.0))/(tf * (1.2 * ((1 - 0.75) + 0.75 * (float(len(doc_tokens))/avg_doc_length))))) * idf  
            
            output_vector[token] = weight_TFIDF           


    return output_vector

# constructing paperid_to_vector_map
def construct_vector_map():
    for doc_id in range(len(paper_list)): 
        paperid_to_vector_map[doc_id] = construct_single_vector(paper_list[doc_id].abstract, doc_id)


if __name__ == '__main__':

    read_doc()
    construct_vector_map()

    doc_id = 0
