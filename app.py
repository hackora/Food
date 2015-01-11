#!/usr/bin/env python

from __future__ import print_function
import sys
import os
from wsgiref.simple_server import make_server
from cgi import escape
import sklearn
import cPickle

import urlparse

html = """
<html>
<body>
   <form method="get" action="parsing_get.wsgi">
      <p>
         Age: <input type="text" name="age">
         </p>
      <p>
         Hobbies:
         <input name="hobbies" type="checkbox" value="software"> Software
         <input name="hobbies" type="checkbox" value="tunning"> Auto Tunning
         </p>
      <p>
         <input type="submit" value="Submit">
         </p>
      </form>
   <p>
      Age: %s<br>
      Hobbies: %s
      </p>
   </body>
</html>"""


def application(environ, start_response):
    # Returns a dictionary containing lists as values.
    d = urlparse.parse_qs(environ['QUERY_STRING'])
    # In this idiom you must issue a list containing a default value.
    ingredients = d.get('ingredients', [])[0].split(',')  # Returns the first age value.
    print(ingredients)
    # Always escape user input to avoid script injection

    # features = []
    # feature_vector = [1 if ingredient == feature else 0 for feature in features]
    #
    # tasty_rating = clf.predict(feature_vector)
    # health_rating =
    tasty_rating = 500
    response = {"ratings": {"health": 0,
                            "rating": tasty_rating}}

    status = '200 OK'
    response_body = str(response)
    response_headers = [('Content-Type', 'application/json'),
                        ('Content-Length', str(len(response_body)))]
    start_response(status, response_headers)

    return [response_body]

with open('clf.pickle', 'rb') as f:
    taste_clf = cPickle.load(f)

httpd = make_server('0.0.0.0', int(os.environ.get('PORT', 5000)), application)
# Now it is serve_forever() in instead of handle_request().
# In Windows you can kill it in the Task Manager (python.exe).
# In Linux a Ctrl-C will do it.
httpd.serve_forever()