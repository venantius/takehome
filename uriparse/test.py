#!/usr/bin/env python
# encoding: utf-8

import uri
import unittest

class TestUriSchemes(unittest.TestCase):
    """
    Test suite for our uri class; checks that the uri class can 
    correctly parse various instances types of URIs. Samples are taken 
    directly from RFP 3986, section 1.1.2 ("Examples"). Some manufactured
    examples are also included to test specific things.
    """
    def setUp(self):
        """Definine our test data with most of the common use cases"""
        # Scheme, host, path
        self.ftp_case = uri.URI.parse_uri('ftp://ftp.is.co.za/rfc/rfc1808.txt')
        # Scheme, ipv6, path, query
        self.ldap_case = uri.URI.parse_uri(
            'ldap://[2001:db8::7]/c=GB?objectClass?one')
        # Path, nothing else
        self.news_case = uri.URI.parse_uri(
            "news:comp.infosystems.www.servers.unix")
        # Path with scheme
        self.urn_case = uri.URI.parse_uri(
            "urn:oasis:names:specification:docbook:dtd:xml:4.1.2")
        # Path with scheme and port
        self.telnet_case = uri.URI.parse_uri("telnet://192.0.2.16:80/")
        # Scheme, authority, path, query, fragment
        self.foo_case = uri.URI.parse_uri(
            "foo://herp@example.com:8042/over/there?name=ferret#nose") 
        self.sld_case = uri.URI.parse_uri(
                "http://www.amazon.co.uk/search/product_page?id=52342")
        # Scheme, host, path, query, fragment
        self.gmail_case = uri.URI.parse_uri(
            'https://www.google.com/search?q=setter+python&oq=setter+python&aqs=chrome..69i57j0l3.9438j0&sourceid=chrome&ie=UTF-8')
        # Same as the above, but from direct initialization
        self.gmail_case_from_init = uri.URI(
            path='/search', scheme='https', authority='www.google.com', 
            query='q=setter+python&oq=setter+python&aqs=chrome..69i57j0l3.9438j0&sourceid=chrome&ie=UTF-8')
        # Pure path with dot segments
        self.dot_case = uri.URI(path='/a/b/c/./../../g')
        # Another pure path with dot segments
        self.dot_case2 = uri.URI(path='mid/content=5/../6')
        # A more complete IPV6 sample, with a port
        self.sample_ipv6_case = uri.URI.parse_uri(
            'http://[FEDC:BA98:7654:3210:FEDC:BA98:7654:3210]:80/index.html')
        # An example with a percent-encoded authority
        self.percent_host = uri.URI(authority='herp%2fballoon', scheme='ftP')

    def test_domain(self):
        """
        Test that we can get and set the domain
        """
        self.assertEqual(self.gmail_case.domain, 'google.com')
        self.gmail_case.domain = 'yahoo.com'
        self.assertEqual(self.gmail_case.domain, 'yahoo.com')
        self.assertEqual(self.sld_case.domain, 'amazon.co.uk')
        self.assertEqual(self.gmail_case.tld, 'com')
        self.assertEqual(self.sld_case.tld, 'co.uk')
        self.gmail_case.tld = 'co.ke'
        self.sld_case.tld = 'gov'
        self.assertEqual(self.gmail_case.tld, 'co.ke')
        self.assertEqual(self.sld_case.tld, 'gov')
        self.assertEqual(self.gmail_case.domain, 'yahoo.co.ke')
        self.assertEqual(self.sld_case.domain, 'amazon.gov')

    def test_changedir(self):
        """
        Test that we can change directories
        """
        self.dot_case.chdir('.')
        self.assertEqual(self.dot_case.__repr__(), '/a/b/c/./../../g/.')
        self.dot_case.chdir('..')
        self.assertEqual(self.dot_case.__repr__(), '/a/b/c/./../../g/./..')
        
        self.dot_case = uri.URI(path='/a/b/c/./../../g')
        self.dot_case.chdir('./')
        self.assertEqual(self.dot_case.__repr__(), '/a/b/c/./../../g/./')
        self.dot_case.chdir('/../')
        self.assertEqual(self.dot_case.__repr__(), '/a/b/c/./../../g/./../')

    def test_query_append(self):
        """
        Test that we can modify the query ad-hoc
        """
        self.assertEqual(self.gmail_case.query_dict, 
                {'aqs': 'chrome..69i57j0l3.9438j0', 'ie': 'UTF-8', 
                    'oq': 'setter+python', 'q': 'setter+python', 
                    'sourceid': 'chrome'})
        self.gmail_case.set_query_arg('Ladies + Gentlemen')
        self.assertEqual(self.gmail_case.query_dict, 
                {'aqs': 'chrome..69i57j0l3.9438j0', 'ie': 'UTF-8', 
                    'oq': 'setter+python', 'q': 'setter+python',
                    'Ladies + Gentlemen': None,
                    'sourceid': 'chrome'})
        self.foo_case.set_query_arg('demo_key', 'demo_value')
        self.assertEqual(self.foo_case.get_query_arg('demo_key'), 'demo_value')

    def test_authority(self):
        """Test that we can identify authority if it exists"""
        self.assertEqual(self.ftp_case.authority, "ftp.is.co.za")
        self.assertEqual(self.ldap_case.authority, "[2001:db8::7]")
        self.assertEqual(self.telnet_case.authority, "192.0.2.16:80")
    
    def test_fragment(self):
        """Test that we can identify a fragment if it exists"""
        self.assertEqual(self.foo_case.fragment, "nose")
    
    def test_path(self):
        """
        Test that the path is initialized and set properly.
        
        In particular:
         -  If a URI contains an authority component, then the path component
            must either be empty or begin with a slash ("/") character.
         - If a URI does not contain an authority component, then the path 
            cannot begin with two slash characters ("//").
        """
        self.assertEqual(self.ftp_case.path, '/rfc/rfc1808.txt')
        self.assertEqual(self.ldap_case.path, '/c=GB')
        self.assertEqual(self.news_case.path, 
                'comp.infosystems.www.servers.unix')
        self.assertEqual(self.telnet_case.path, '/')
        self.assertEqual(self.urn_case.path, 
                'oasis:names:specification:docbook:dtd:xml:4.1.2')

    def test_port(self):
        """Test that we can identify port if it exists"""
        self.assertEqual(self.gmail_case.port, None)
        self.assertEqual(self.telnet_case.port, 80)
        self.assertEqual(self.foo_case.port, 8042)

    def test_query(self):
        """Test that we can identify a query if it exists"""
        self.assertEqual(self.ftp_case.query, None)
        self.assertEqual(self.ldap_case.query, 'objectClass?one')
        self.assertEqual(self.foo_case.query, 'name=ferret')
        self.assertEqual(self.gmail_case.query, 'q=setter+python&sourceid=chrome&ie=UTF-8&aqs=chrome..69i57j0l3.9438j0&oq=setter+python')

    def test_userinfo(self):
        """Test that we can identify the userinfo if it exists"""
        self.assertEqual(self.gmail_case.userinfo, None)
        self.assertEqual(self.foo_case.userinfo, 'herp')

    def test_repr(self):
        """
        Test that we can re-constitute the URI
        """
        self.assertEqual(self.ftp_case.__repr__(), 
                'ftp://ftp.is.co.za/rfc/rfc1808.txt')
        self.assertEqual(self.ldap_case.__repr__(), 
                'ldap://[2001:db8::7]/c=GB?objectClass?one')
        self.assertEqual(self.telnet_case.__repr__(),
                "telnet://192.0.2.16:80/")
        self.assertEqual(self.urn_case.__repr__(), 
                "urn:oasis:names:specification:docbook:dtd:xml:4.1.2")
        self.assertEqual(self.dot_case.__repr__(), "/a/b/c/./../../g")
        self.assertEqual(self.dot_case2.__repr__(), "mid/content=5/../6")
        self.assertEqual(self.dot_case.__repr__(normalize=True), "/a/g")
        self.assertEqual(self.dot_case2.__repr__(normalize=True), "mid/6")
        # Test that we keep the right things upper and lower cased
        self.assertEqual(self.percent_host.__repr__(normalize=True), 
                'ftp://herp%2Fballoon/')
        self.assertEqual(self.percent_host.__repr__(normalize=False), 
                'ftP://herp%2fballoon')

    def test_eq(self):
        """
        Test that we can do valid comparisons
        """
        self.assertEqual(self.gmail_case, self.gmail_case_from_init)

    def test_scheme(self):
        """Test that we can parse the URI scheme correctly"""
        self.assertEqual(self.ftp_case.scheme, "ftp")
        self.assertEqual(self.ldap_case.scheme, "ldap")
        self.assertEqual(self.news_case.scheme, "news")
        self.assertEqual(self.telnet_case.scheme, "telnet")
        self.assertEqual(self.urn_case.scheme, "urn")

    def test_percent_encode(self):
        """Test that we can percent-encode an argument properly"""
        self.gmail_case.set_query_arg('Ladies + Gentlemen')
        self.assertEqual(self.gmail_case.__repr__(), 
                'https://www.google.com/search?aqs=chrome..69i57j0l3.9438j0&sourceid=chrome&Ladies%20+%20Gentlemen&q=setter+python&ie=UTF-8&oq=setter+python')

    def test_percent_decode(self):
        """Test that we can decode a percent-encoded argument properly"""
        new_case = uri.URI.parse_uri('https://www.google.com/search?aqs=chrome..69i57j0l3.9438j0&sourceid=chrome&Ladies%20+%20Gentlemen&q=setter+python&ie=UTF-8&oq=setter+python')
        self.assertEqual(new_case.get_query_arg('Ladies + Gentlemen'), None)

if __name__ == "__main__":
    unittest.main()
