#!/usr/bin/env python
# encoding: utf-8

"""
A light Tornado application that allows for search via fuzzy substring matching.

Returns results as a JSON-blog of the form: {"results": ["result_1", ...]}
"""

import difflib
import json
import tornado.ioloop
import tornado.web

from collections import defaultdict

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
    def initialize(self, substring_dict, substring_set):
        self.substring_dict = substring_dict
        self.substring_set = substring_set

    def add_substrings(self, string):
        """
        Calculates all substrings for the given string. Using each substring as 
        the key, adds the original string to the dictionary's set (in the value 
        position)
        
        Useful for O(1) lookups of search terms, though a little expensive here
        in the computation.
        """
        for i in range(len(string)):
            for j in range(len(string[i:])):
                self.substring_dict[string[i:len(string) - j]].add(string)
                self.substring_set.add(string[i:len(string) - j])

    def post(self):
        self.set_header("Content-Type", "text/plain")
        self.write("You wrote " + self.get_argument("string"))
        self.add_substrings(self.get_argument("string"))

class SearchHandler(tornado.web.RequestHandler):
    """
    A handler to return search results
    """
    def initialize(self, substring_dict, substring_set):
        self.substring_dict = substring_dict
        self.substring_set = substring_set

    def fuzzy_match(self, search_substring):
        for substring in self.substring_set:
            if difflib.SequenceMatcher(None, search_substring, substring)\
                    .ratio() > 0.6:
                return substring
        return None

    def get(self, search_substring):
        if len(self.substring_dict[search_substring]) > 0:
            self.write(json.dumps({'results': sorted(
                self.substring_dict[search_substring])}))
        else:
            self.write(json.dumps({'results': sorted(
                self.substring_dict[self.fuzzy_match(search_substring)])}))

substring_dict = defaultdict(set)
substring_set = set()
application = tornado.web.Application([
    (r"/formsubmit", FormHandler),
    (r"/add", AddHandler, dict(substring_dict=substring_dict,
        substring_set=substring_set)),
    (r"/search/([a-zA-Z]+)", SearchHandler, 
        dict(substring_dict=substring_dict, substring_set=substring_set)),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
