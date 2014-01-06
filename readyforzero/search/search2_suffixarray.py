#!/usr/bin/env python
# encoding: utf-8

"""
A light Tornado application that allows for search via fuzzy substring matching. 
This particular extension uses a suffix array, with the core data structure
implementation in suffixarray.py

Returns results as a JSON-blog of the form: {"results": ["result_1", ...]}
"""

import json
import suffixarray
import tornado.ioloop
import tornado.web

from collections import defaultdict
from string import letters # [a-zA-Z]

class FormHandler(tornado.web.RequestHandler):
    """
    Including a form that can be used to add strings to the dictionary.
    """
    def get(self):
        self.write('<html><body><form action="/add" method="post">'
                '<input type="text" name="string">'
                '<input type="submit" value="Submit">'
                '</form></body></html>')

class AddHandler(tornado.web.RequestHandler):
    """
    Handler for adding strings
    """
    def initialize(self, suffix_array):
        self.suffix_array = suffix_array

    def post(self):
        self.set_header("Content-Type", "text/plain")
        self.write("You wrote " + self.get_argument("string"))
        self.suffix_array.insert(self.get_argument("string"))

class SearchHandler(tornado.web.RequestHandler):
    """
    A handler to return search results
    """
    def initialize(self, suffix_array):
        self.suffix_array = suffix_array

    def get(self, substring):
        self.write(json.dumps({'results': sorted(
            self.suffix_array.get_fuzzy_search_results(substring))}))

suffix_array = suffixarray.SuffixArray()
application = tornado.web.Application([
    (r"/formsubmit", FormHandler),
    (r"/add", AddHandler, dict(suffix_array=suffix_array)),
    (r"/search/([a-zA-Z]+)", SearchHandler, 
        dict(suffix_array=suffix_array)),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
