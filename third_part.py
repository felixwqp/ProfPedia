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

def get_score_for_paper(query, paperid):
  #output: score for paperid
  pass

def get_score_for_profs(query):
    profs_to_score_map = {}
    for prof, paperid_list in prof_to_paperids_map.items():
        max_score = 0
        for paperid in paperid_list:
            current_score = get_score_for_paper(query, paperid)
            if current_score > max_score:
                max_score = current_score
        profs_to_score_map[prof] = max_score
    return profs_to_score_map


def prof_in_constraints(prof_name, university, field):
    prof_info = prof_to_info_map[prof_name]
    if university == prof_info.university and field == prof_info.field:
        return True 
    else:
        return False 

def main():
    print("This is ")



  pass


if __name__ == '__main__':
    main()
