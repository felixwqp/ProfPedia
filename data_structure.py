  

class Paper
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
paperid_to_vector_map = {}
paperid_to_words_of_title = {}
inverted_index = {}

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
  pass


def get_score_for_profs(query):
  #output: profs_to_score_map
  pass

def prof_in_constraints(prof_name, university, field)
  pass

def handle_query(query):
  pass

def main():
  pass

Test cases:
Input: phrase and university and field
Output: 
