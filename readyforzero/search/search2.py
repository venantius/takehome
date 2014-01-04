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
    def initialize(self, substring_dict):
        self.substring_dict = substring_dict

    def add_substrings(self, variant_string, actual_string):
        """
        Calculates all substrings for the given string. Using each substring as 
        the key, adds the original string to the dictionary's set (in the value 
        position)
        
        Useful for O(1) lookups of search terms, though a little expensive here
        in the computation.
        """
        for i in range(len(variant_string)):
            for j in range(len(variant_string[i:])):
                self.substring_dict[variant_string[i:len(variant_string) - j]]\
                        .add(actual_string)

    def generate_variants(self, input_string, alphabet=letters):
        """
        For each letter in the input string, substitute all possible letters
        in that space and return a list of all words with such substitutions.

        By default, uses letter substitution (i.e. [a-zA-Z]), but other 
        alphabets can easily be substituted in
        """
        strings = []
        for x in range(len(input_string)):
            for char in letters:
                strings.append(input_string[:x] + char + input_string[x+1:])
        return strings

    def post(self):
        self.set_header("Content-Type", "text/plain")
        self.write("You wrote " + self.get_argument("string"))
        original_string = self.get_argument("string")
        string_variants = self.generate_variants(original_string)
        for string_variant in string_variants:
            self.add_substrings(string_variant, original_string)

class SearchHandler(tornado.web.RequestHandler):
    """
    A handler to return search results
    """
    def initialize(self, substring_dict):
        self.substring_dict = substring_dict

    def get(self, substring):
        self.write(json.dumps({'results': sorted(self.substring_dict[substring])}))

substring_dict = defaultdict(set)
application = tornado.web.Application([
    (r"/formsubmit", FormHandler),
    (r"/add", AddHandler, dict(substring_dict=substring_dict)),
    (r"/search/([a-zA-Z]+)", SearchHandler, 
        dict(substring_dict=substring_dict)),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
