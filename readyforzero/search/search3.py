#!/usr/bin/env python
# encoding: utf-8

"""
A light Tornado application that checks to see if a string exists via substring 
matching.

Returns results as a JSON-blog of the form: {"results": True} (or False)
"""

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
    def initialize(self, substring_set):
        self.substring_set = substring_set

    def add_substrings(self, string):
        """
        Calculates all substrings for the given string, then adds them to the 
        substring set.
        
        This approach is good for simply testing if a search term exists or 
        not, though it cannot be used to retrieve the actual search term.
        """
        for i in range(len(string)):
            for j in range(len(string[i:])):
                self.substring_set.add(string[i:len(string) - j])

    def post(self):
        self.set_header("Content-Type", "text/plain")
        self.write("You wrote " + self.get_argument("string"))
        self.add_substrings(self.get_argument("string"))

class SearchHandler(tornado.web.RequestHandler):
    """
    A handler to return search results
    """
    def initialize(self, substring_set):
        self.substring_set = substring_set

    def get(self, substring):
        if substring in self.substring_set:
            self.write(json.dumps({'results': True}))
        else:
            self.write(json.dumps({'results': False}))

substring_set = set()
application = tornado.web.Application([
    (r"/formsubmit", FormHandler),
    (r"/add", AddHandler, dict(substring_set=substring_set)),
    (r"/search/([a-zA-Z]+)", SearchHandler, 
        dict(substring_set=substring_set)),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
