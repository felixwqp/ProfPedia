"""
Profpedia index (main) view.

URLs include:
/
"""
import os
import re
import flask
import profpedia 
import requests

PROFS = [
    {
      "prof_name": "Rada Mihalcea",
      "homepage" : "https://web.eecs.umich.edu/~mihalcea/",
    },
    {
      "prof_name": "Rada Mihalcea",
      "homepage" : "https://web.eecs.umich.edu/~mihalcea/",
    },
    {
      "prof_name": "Rada Mihalcea",
      "homepage" : "https://web.eecs.umich.edu/~mihalcea/",
    },
    {
      "prof_name": "Rada Mihalcea",
      "homepage" : "https://web.eecs.umich.edu/~mihalcea/",
    },
    {
      "prof_name": "Rada Mihalcea",
      "homepage" : "https://web.eecs.umich.edu/~mihalcea/",
    }
  ]

@profpedia.app.route('/', methods=['GET'])
def show_index():
    """Show index page."""
    context = {}
    return flask.render_template("search.html", **context)


@profpedia.app.route('/api/v1/search/q=<query>', methods=["POST"])
def handle_query(query):
    print("enter handle query")
    #url = "http://{host}:{port}?w=" + str(w) + "&q=" + str(query)
    #results = requests.get(url).content.decode('utf-8')

    """
    connection = get_db()
    docs = []
    for doc_info in hits:
        new_doc = {}
        new_doc["docid"] = int(doc_info["docid"])
        cur = connection.cursor().execute( "SELECT * from Documents WHERE docid = %d;" % int(doc_info["docid"])).fetchone()
        new_doc["title"] = cur["title"]
        new_doc["title"] = re.sub(r'\_', ' ', new_doc["title"])
        new_doc["summary"] = cur["summary"]
        docs.append(new_doc)
    """
    
    context = {}
    context["profs"] = PROFS
    #context["docs"] = docs
    return flask.jsonify(**context)
  
def search(query):
  pass