# -*- coding: utf-8 -*-
import os
import sys
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import string
import math
import operator
import pickle


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
    def __init__(self):
        self.name = ""
        self.homepage_url = ""
        self.university = ""
        self.field = []


# name of prof - > prof class?
prof_to_info_map = dict()
# prof -> list of doc_ids
prof_to_paperids_map = dict()
paperid_to_vector_map = dict()
paperid_to_length = dict()
# id -> set of words
paperid_to_words_of_title = dict()
# term -> df & tf for each doc which is a double dimension dict
# inverted_index doesnt store the title !!!
inverted_index = dict()

#univeristy to set of profs  //set for look uo efficiency
university_to_prof = dict()
#field to set of profs
field_to_prof = dict()

paper_list = []

doc_id = 0
avg_doc_length = 0.0


# read each file from dir "papers"

def read_in_prof_homepage():
    for prof_name, prof_info in prof_to_info_map.items():
        try:
            each_file = open(os.path.join('profs', prof_name), 'r').read().splitlines() 
        except:
            print(prof_name)
        prof_info.homepage_url = each_file[0]
    
    
    
def read_doc():
    global doc_id
    global inverted_index
    global prof_to_paperids_map
    global paperid_to_words_of_title
    global prof_to_info_map
    global paper_list
    global avg_doc_length

    papers_dir = os.listdir('papers')

    for i in range(len(papers_dir)):
        try:
            each_file = open(os.path.join('papers', papers_dir[i]), 'r').read().splitlines() 
        except:
            print(papers_dir[i])
        j = 0
        prof_name = papers_dir[i]
        temp_prof = Professor()
        temp_prof.name = prof_name
        # TODO:
        # add in other basic info for each prof
        prof_to_info_map[prof_name] = temp_prof

        # if none element in professor txt, it should skip the while loop
        while j < len(each_file):
            currPaper = Paper()
            # title
            title = preprocesss(each_file[j])
            currPaper.title = title
            '''
            if prof_name not in prof_to_paperids_map:
                prof_to_paperids_map[prof_name] = list()
            prof_to_paperids_map[prof_name].append(doc_id)

            doc_id = doc_id + 1
            '''
            # abstract
            abstract = preprocesss(each_file[j + 2])
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

    avg_doc_length /= len(paper_list)

    # indexDocument(each_doc, doc_weighting, query_weighting, inverted_index)


    
def read_university_field():
    global prof_to_info_map
    global university_to_prof
    global field_to_prof
    
    
    #read in the university to prof  
    university_dir = os.listdir('universities')
    for i in range(len(university_dir)):
        try:
            each_university_file = open(os.path.join('universities', university_dir[i]), 'r').read().splitlines() 
            #print(university_dir[i][:-4])
        except:
            print("not a valid univeristy file")
        current_university = university_dir[i][:-4]
        for j in range(len(each_university_file)):
            if each_university_file[j] in prof_to_info_map:
                prof_to_info_map[each_university_file[j]].university = current_university
            if current_university not in university_to_prof:
                university_to_prof[current_university] = set()             
            university_to_prof[current_university].add(each_university_file[j])
    
    #read in the fields
    field_dir = os.listdir('fields')
    for i in range(len(field_dir)):
        sub_path = os.path.join('fields', field_dir[i])
        sub_field_dir = os.listdir(sub_path)
        for j in range(len(sub_field_dir)):
            each_sub_field_file = open(os.path.join(sub_path, sub_field_dir[j]), 'r').read().splitlines()
            for k in range(len(each_sub_field_file)):
                if each_sub_field_file[k] in prof_to_info_map:
                    prof_to_info_map[each_sub_field_file[k][:-1]].field.append(sub_field_dir[j])
                    print(prof_to_info_map[each_sub_field_file[k][:-1]].field)
                if sub_field_dir[j] not in field_to_prof:
                    field_to_prof[sub_field_dir[j]] = set()
                field_to_prof[sub_field_dir[j]].add(each_sub_field_file[k][:-1])
          
   # print("Hu Ding" in field_to_prof['ai'])
            
            
            

   # for i in range()
    
    
# pass each doc (title/abstract) and return the list of tokens
# remove stopword  & porter stemming
def preprocesss(doc_str):
    ps = PorterStemmer()
    '''
    for i in range(len(doc_str)):
      for punctuation in string.punctuation:
        doc_str[i] = doc_str[i].replace(punctuation, ' ')
    '''
    doc_str = nltk.word_tokenize(doc_str)
    doc_str = [word for word in doc_str if word not in stopwords.words(
        'english') or word not in string.punctuation]

    output_str = []
    for word in doc_str:
        output_str.append(ps.stem(word))

    return output_str


# layout of inverted_index  {each_term:{(0:df), (docid:tf)}}


def cal_inverted_index(each_doc, docid, inverted_index):
    for term in each_doc:
        if term in inverted_index:
            if docid in inverted_index[term]:
                inverted_index[term][docid] = inverted_index[term][docid] + 1
            else:
                inverted_index[term][docid] = 1
                # inverted_index[term][0] is doc frequency of each term
                inverted_index[term][0] = inverted_index[term][0] + 1
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

    doc_length = 0
    for token in uniqueTokens:
        if token in inverted_index:
            tf = (float(inverted_index[token][docid]) / float(maxFreq))
            idf = math.log10(float(len(paper_list)) /
                             float(inverted_index[token][0]))

            # tf-idf weights
            weight_TFIDF = tf * idf
            # BM-25 weights, with tuning factors k1 = 1.2, b = 0,75
            weight_BM = ((tf * (1.2 + 1.0)) / (tf * (1.2 * ((1 - 0.75) +
                                                            0.75 * (float(
                        len(doc_tokens)) / avg_doc_length))))) * idf

            output_vector[token] = weight_TFIDF
            doc_length += (output_vector[token] * output_vector[token])
    doc_length = math.sqrt(doc_length)
    paperid_to_length[docid] = doc_length
    return output_vector


# constructing paperid_to_vector_map


def construct_vector_map():
    for doc_id in range(len(paper_list)):
        paperid_to_vector_map[doc_id] = construct_single_vector(
            paper_list[doc_id].abstract, doc_id)


def get_score_for_paper(query, paperid):
    # output: score for paperid
    paperVector = paperid_to_vector_map[paperid]
    titleSet = paperid_to_words_of_title[paperid]
    query_word_list = preprocesss(query)

    # recorded the tf and max tf

    # construct query vector
    maxFreq = 0
    query_vector = {}
    for word in query_word_list:
        if word not in query_vector:
            query_vector[word] = 0
        query_vector[word] += 1
        if query_vector[word] > maxFreq:
            maxFreq = query_vector[word]

        # calculate word weight and if word in title, score *= 2
    query_length = 0
    for word, score in query_vector.items():
        if word in titleSet:
            score *= 2
        score = score / maxFreq
        query_length += (score * score)

    query_length = math.sqrt(query_length)
    paper_length = paperid_to_length[paperid]

    total_score = 0
    for word, score in query_vector.items():
        if word in paperVector:
            total_score += score * paperVector[word]

    if paper_length == 0:
        print(paperid)
        print(paperVector)
    if query_length == 0:
        print(query)

    total_score /= (query_length * paper_length)

    return total_score


def get_score_for_profs(query):
    # score: maxscore + avgscore of paper
    profs_to_score_map = {}
    for prof, paperid_list in prof_to_paperids_map.items():
        total_score = 0
        max_score = 0
        for paperid in paperid_list:
            current_score = get_score_for_paper(query, paperid)
            if current_score > max_score:
                max_score = current_score
            total_score += current_score
        profs_to_score_map[prof] = max_score + total_score / len(paperid_list)
    return profs_to_score_map


def prof_in_constraints(prof_name, university, field):
    prof_info = prof_to_info_map[prof_name]
    try:
        if university == prof_info.university and field == prof_info.field:
            return True
        else:
            return False
    except:
        return False


def handle_query(query, university, field):
    #TODO:
    #add the univerisity and filed to be the filter!!!!!!!!!!!!!!!!!
    profs_to_score_map = get_score_for_profs(query)
    rankedProfs = list({k: v for k, v in sorted(
        profs_to_score_map.items(), key=lambda x: x[1], reverse=True)}.items())
    count = 0
    print("enter query")
    for prof, score in rankedProfs:
        if prof_in_constraints(prof, university, field):
            count += 1
            print(str(count) + ": " + prof)
            print("Homepage: " + prof_to_info_map[prof].homepage_url)
            print("Score: " + str(score))
        if count == 10:
            break


def printProf(profName):
    # f = open(profName, 'r')
    print(profName)
    profInfo = prof_to_info_map[profName]
    print(profInfo.home)
    # f.close()


"""
def main():

    query = "machine learning"
    while (query != ""):
        handle_query(query)
    pass
    """

def usage():
    print("This is ProfPedia Search Engine")
    print("Usage: python profpedia_total.py <query_doc>")
    print("query_doc: ")
    print("Line 1: query")
    print("Line 2: university")
    print("Line 3: field")

def move_file():
    file = open(os.getcwd()+"/universities/University_of_Michigan.txt","r")
    namelist = []

    line = file.readline()

    while line:
        name = line.strip("\n")
        namelist.append(name)
        line = file.readline()
    
    for name in namelist:
        try:
            each_file = open(os.path.join('papers/', name), 'r').read()
            save_file = open(os.path.join('papers_test2/', name), 'w')
            save_file.write(each_file)
        except:
            continue

    

if __name__ == '__main__':
    """
    if len(sys.argv) != 2:
        usage()
        exit()
    """


    move_file()
    read_doc()
    read_university_field()

    """
    read_in_prof_homepage()
    construct_vector_map()
    print("Finish reading")

    file = open("prof_to_info_map.pickle", 'wb')
    pickle.dump(prof_to_info_map, file)
    file.close

    file = open("prof_to_paperids_map.pickle", 'wb')
    pickle.dump(prof_to_paperids_map, file)
    file.close

    file = open("paperid_to_vector_map.pickle", 'wb')
    pickle.dump(paperid_to_vector_map, file)
    file.close

    file = open("paperid_to_length.pickle", 'wb')
    pickle.dump(paperid_to_length, file)
    file.close

    file = open("paperid_to_words_of_title.pickle", 'wb')
    pickle.dump(paperid_to_words_of_title, file)
    file.close


    file = open("inverted_index.pickle", 'wb')
    pickle.dump(inverted_index, file)
    file.close
    """

    file = open("prof_to_info_map.pickle", 'rb')
    prof_to_info_map = pickle.load(file)
    file.close

    file = open("prof_to_paperids_map.pickle", 'rb')
    prof_to_paperids_map = pickle.load(file)
    file.close

    file = open("paperid_to_vector_map.pickle", 'rb')
    paperid_to_vector_map = pickle.load(file)
    file.close

    file = open("paperid_to_length.pickle", 'rb')
    paperid_to_length = pickle.load(file)
    file.close

    file = open("paperid_to_words_of_title.pickle", 'rb')
    paperid_to_words_of_title = pickle.load(file)
    file.close

    file = open("inverted_index.pickle", 'rb')
    inverted_index = pickle.load(file)
    file.close
    #print(prof_to_info_map)
    

    """
    test_prof_name = "Vibhav Gogate"
    prof_info = prof_to_info_map[test_prof_name]
    print("Name: " + prof_info.name)
    #print("Homepage: " + prof_info.homepage_url)
    print("Univeristy: " + prof_info.university)
    print( prof_info.field)
    """


    while 1:
        query = input("Query: ")
        university = input("University: ")
        field = input("field: ")
        handle_query(query, university, field)
  
