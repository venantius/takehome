#!/usr/bin/env python
# encoding: utf-8

"""
Some tests for our search application
"""

import search1
import search2
import search3

import json
import tornado.testing
import unittest
import urllib

class TestSearch1(tornado.testing.AsyncHTTPTestCase):
    """
    Test extension 1 of our search application
    """
    def get_app(self):
        return search1.application

    def setUp(self):
        """
        Put in Alabama and Arkansas
        """
        super(TestSearch1, self).setUp()
        payload = urllib.urlencode({'string': 'Alabama'})
        payload2 = urllib.urlencode({'string': 'Arkansas'})
        self.fetch('/add', method='POST', body=payload)
        self.fetch('/add', method='POST', body=payload2)

    def testGetArk(self):
        """
        Test what happens when we search for 'Ark'
        """
        x = self.fetch('/search/Ark', method="GET")
        results = json.loads(x.buffer.read())
        self.assertEqual(results['results'], ["Arkansas"])
    
    def testGeta(self):
        """
        Test what happens when we search for 'a'
        """
        x = self.fetch('/search/a', method="GET")
        results = json.loads(x.buffer.read())
        self.assertEqual(results['results'], ["Alabama", "Arkansas"])

    def testGetBanana(self):
        """
        Test what happens when we search for 'Banana'
        """
        x = self.fetch('/search/Banana', method="GET")
        results = json.loads(x.buffer.read())
        self.assertEqual(results['results'], [])

class TestSearch2(tornado.testing.AsyncHTTPTestCase):
    """
    Test extension 2 of our search application
    """
    def get_app(self):
        return search2.application

    def setUp(self):
        """
        Put in Alabama and Arkansas
        """
        super(TestSearch2, self).setUp()
        payload = urllib.urlencode({'string': 'Alabama'})
        payload2 = urllib.urlencode({'string': 'Arkansas'})
        self.fetch('/add', method='POST', body=payload)
        self.fetch('/add', method='POST', body=payload2)

    def testGetArk(self):
        """
        Test what happens when we search for 'Ark'
        """
        x = self.fetch('/search/Ark', method="GET")
        results = json.loads(x.buffer.read())
        self.assertEqual(results['results'], ["Arkansas"])
    
    def testGeta(self):
        """
        Test what happens when we search for 'a'
        """
        x = self.fetch('/search/a', method="GET")
        results = json.loads(x.buffer.read())
        self.assertEqual(results['results'], ["Alabama", "Arkansas"])

    def testGetBanana(self):
        """
        Test what happens when we search for 'Banana'
        """
        x = self.fetch('/search/Banana', method="GET")
        results = json.loads(x.buffer.read())
        self.assertEqual(results['results'], [])
class TestSearch3(tornado.testing.AsyncHTTPTestCase):
    """
    Test extension 3 of our search application
    """
    def get_app(self):
        return search3.application

    def setUp(self):
        """
        Put in Alabama and Arkansas
        """
        super(TestSearch3, self).setUp()
        payload = urllib.urlencode({'string': 'Alabama'})
        payload2 = urllib.urlencode({'string': 'Arkansas'})
        self.fetch('/add', method='POST', body=payload)
        self.fetch('/add', method='POST', body=payload2)

    def testGetArk(self):
        """
        Test what happens when we search for 'Ark'
        """
        x = self.fetch('/search/Ark', method="GET")
        results = json.loads(x.buffer.read())
        self.assertEqual(results['results'], True)
    
    def testGeta(self):
        """
        Test what happens when we search for 'a'
        """
        x = self.fetch('/search/a', method="GET")
        results = json.loads(x.buffer.read())
        self.assertEqual(results['results'], True)

    def testGetBanana(self):
        """
        Test what happens when we search for 'Banana'
        """
        x = self.fetch('/search/Banana', method="GET")
        results = json.loads(x.buffer.read())
        self.assertEqual(results['results'], False)

if __name__ == "__main__":
    unittest.main()
