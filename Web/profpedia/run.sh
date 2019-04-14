export FLASK_DEBUG=True
export FLASK_APP=profpedia
export SEARCH_SETTINGS=config.py
./node_modules/.bin/webpack
flask run --host 0.0.0.0 --port 8000