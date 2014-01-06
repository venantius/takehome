#!/usr/bin/env python
# encoding: utf-8

"""
Some tests for our search application
"""

import search1
import search2
import search2_suffixarray
import search3
import suffixarray

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
    
    def testGetAlam(self):
        """
        Test what happens when we search for 'Alam'
        """
        x = self.fetch('/search/Alam', method="GET")
        results = json.loads(x.buffer.read())
        self.assertEqual(results['results'], ["Alabama"])

    def testGetAlaba(self):
        """
        Test what happens when we search for 'Alaba'
        """
        x = self.fetch('/search/Alaba', method="GET")
        results = json.loads(x.buffer.read())
        self.assertEqual(results['results'], ["Alabama"])

    def testGetBanana(self):
        """
        Test what happens when we search for 'Banana'
        """
        x = self.fetch('/search/Banana', method="GET")
        results = json.loads(x.buffer.read())
        self.assertEqual(results['results'], [])

class TestSearch2SuffixArray(tornado.testing.AsyncHTTPTestCase):
    """
    Test extension 2 of our search application, using suffix arrays
    """
    def get_app(self):
        return search2_suffixarray.application

    def setUp(self):
        """
        Put in Alabama and Arkansas
        """
        super(TestSearch2SuffixArray, self).setUp()
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
    
    def testGetAlam(self):
        """
        Test what happens when we search for 'Alam'
        """
        x = self.fetch('/search/Alam', method="GET")
        results = json.loads(x.buffer.read())
        self.assertEqual(results['results'], ["Alabama"])

    def testGetAlaba(self):
        """
        Test what happens when we search for 'Alaba'
        """
        x = self.fetch('/search/Alaba', method="GET")
        results = json.loads(x.buffer.read())
        self.assertEqual(results['results'], ["Alabama"])

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

class testSuffixArray(unittest.TestCase):
    """
    Tests for the the Suffix Array data structure.
    """
    def setUp(self):
        """
        Initialize our suffix array
        """
        self.suffix_array = suffixarray.SuffixArray()

    def testInsert(self):
        """
        Make sure that our suffix array is being properly sorted after 
        insertion
        """
        self.suffix_array.insert('Alabama')
        self.assertEquals(self.suffix_array.array, ['Alabama', 'a', 'abama', 'ama', 'bama', 'labama', 'ma'])

    def test_FuzzySearch(self):
        """
        Test a search of 'alam' on the hidden _fuzzy_search method
        """
        self.suffix_array.insert('Alabama')
        self.assertEquals(['abama', 'labama'], 
                self.suffix_array._fuzzy_search('aban'))

    def test_FuzzySearchResults(self):
        """
        Test a search of 'alam' on the public fuzzy search method
        """
        self.suffix_array.insert('Alabama')
        self.assertEquals(set(['Alabama']), 
                self.suffix_array.get_fuzzy_search_results('aban'))

if __name__ == "__main__":
    unittest.main()
