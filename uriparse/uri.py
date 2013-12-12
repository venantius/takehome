#!/usr/bin/env python
# encoding: utf-8

"""
Module intended to meet specifications for a URI as laid out in RFC 3986. 
Includes a number of helpful functions for URI manipulation.
"""

import regexes
from publicsuffix import PublicSuffixList

class URI(object):
    """
    Core URI class as specified in RFC 3986.
    """
    suffix_list = PublicSuffixList()
    def __init__(self, scheme = None, authority = None, path = '', 
            query = None, fragment = None):
        """
        Constitute a URI from various constituent parts. Requires a path,
        but other arguments are optional. Existing URIs will be percent-decoded
        as they are read, but re-encoded when printed or when certain objects
        (such as query or authority strings) are retrieved.

        To create the appropriate object for the following URI:

        >>> demo_uri = 'https://www.google.com/search?q=setter+python&oq=setter+python&aqs=chrome..69i57j0l3.9438j0&sourceid=chrome&ie=UTF-8'

        Either use: 
        
        >>> x = URI.parse_uri(demo_uri) 
        
        or initialize individual components, e.g.:

        >>> x = URI(path = '/search', scheme = 'https', authority = 'www.google.com', 
        query = 'q=setter+python&oq=setter+python&aqs=chrome..69i57j0l3.9438j0&sourceid=chrome&ie=UTF-8')

        Additional query arguments can be easily added as follows:

        >>> x.set_query_arg('bananas', 'are_yummy!')
        """
        self.scheme = scheme
        self._userinfo, self._host, self._port = None, None, None
        self.authority = authority
        self.path = path
        self.query_dict = {}
        self.query = query
        self.fragment = fragment

    def __repr__(self, normalize = False):
        """
        Retrieves the string representation of the URI.

        Assembles the various URI components into a string representation,
        complete with percent-encoding. Can be normalized, which compresses
        dot-segments.

        Args:
            normalize: removes dot-segments
        """
        result = ""
        if self.scheme:
            if normalize: 
                result += self.scheme.lower() + ":"
            else:
                result += self.scheme + ":"
        if self.authority:
            self._build_authority(normalize=normalize)
            result += '//' + self._authority
        if normalize:
            if not self.path:
                result += '/'
            else:
                result += self._remove_dot_segments(self.path)
        else:
            result += self.path
        if self.query:
            result += '?' + self.query
        if self.fragment:
            result += '#' + self.fragment

        # Go through and uppercase any percent-encodings
        if normalize:
            tmp = result
            while tmp.rfind('%') != -1:
                pos = tmp.rfind('%')
                tmp = tmp[:pos]
                result = result[:pos] + result[pos:pos+3].upper() + \
                    result[pos+3:]
            result.find('%')
        return result

    def __eq__(self, other):
        if self.__class__ == other.__class__:
            return (self.__repr__(normalize=True) == 
                    other.__repr__(normalize=True))
        # In case we're just comparing against a URI string
        elif type(other) == str:
            return self.__repr__() == other.lower()
        else:
            return False

    @property
    def authority(self):
        """
        Retrieves a percent-encoded authority string, if one exists.
        """
        self._build_authority()
        return self._authority

    @authority.setter
    def authority(self, authority):
        """
        Sets the authority string and parses the userinfo, host and port.
        """
        self._authority = authority
        self._parse_authority()

    @property
    def domain(self):
        """
        Returns the domain for the given URI.
        """
        if not (self._is_ipv4(self._host) or self._is_ipvliteral(self._host)):
            return self.suffix_list.get_public_suffix(self.host)
        else:
            return None

    @domain.setter
    def domain(self, domain):
        """
        Set the domain for the given URI.
        """
        if not (self._is_ipv4(self._host) or self._is_ipvliteral(self._host)):
            self.host = self.host.split(self.domain)[0] + domain
        else:
            raise Exception, "Host is an IP address, not a domain"

    @property
    def fragment(self):
        """
        Retrieves a percent-encoded fragment, if one exists.
        """
        if self._fragment:
            return self.percent_encode(self._fragment, regexes.FRAGMENT_REGEX)
        else:
            return self._fragment

    @fragment.setter
    def fragment(self, fragment):
        """
        Sets the fragment.
        """
        if fragment:
            self._fragment = self.percent_decode(fragment)
        else:
            self._fragment = None

    @property
    def host(self):
        """
        Retrieve the percent-encoded host, if one has been set. 
        """
        if self._is_ipv4(self._host) or self._is_ipvliteral(self._host):
            return self._host
        else:
            return self.percent_encode(self._host, 
                    regexes.REG_NAME_ELIGIBLE_REGEX)

    @host.setter
    def host(self, host):
        """
        Set a new host for this URI.
        """
        if host == '':
            host = None
        self._host = self.percent_decode(host)

    @property
    def path(self):
        """
        Retrieve the path for this URI
        """
        if self.scheme:
            return '/'.join([self.percent_encode(x, 
                regexes.PATH_REGEX) for x in self._path])
        else:
            return '/'.join([self.percent_encode(x, 
                regexes.PATH_NOSCHEME_REGEX) for x in self._path])

    @path.setter
    def path(self, path):
        """
        Set a new path for this URI
        """
        if self.authority and path != '':
            if path[0] != '/':
                raise Exception, "Invalid path: when authority is present," + \
                    " path should begin with a '/' character"
        elif not self.authority:
            if path[0:2] == '//':
                raise Exception, "Invalid path: when no authority is" + \
                    " present, path cannot begin with '//'"
        self._path = [self.percent_decode(x) for x in path.split('/')]
    
    @property
    def port(self):
        """
        Retrieve the port, if one has been set.
        """
        return self._port
    
    @port.setter
    def port(self, port):
        """
        Set a new port for this URI. 
        
        If a host has been defined, re-build the authority string, else pass 
        (an authority string with no host is meaningless).
        
        Args:
            port: the target port
        """
        self._port = int(port)
    
    @property
    def query(self):
        """
        Retrieves a percent-encoded query string, if one has been set.
        """
        self._build_query()
        if self._query:
            return self.percent_encode(self._query, regexes.QUERY_REGEX)
        else:
            return None
    
    @query.setter
    def query(self, query):
        """
        Sets the query string.
        """
        if query:
            self._query = self.percent_decode(query)
            self._parse_query()
        else:
            self._query = None

    @property
    def tld(self):
        """
        Retrieves the top-level domain, if one has been set.
        """
        return '.'.join(self.domain.split('.')[1:])

    @tld.setter
    def tld(self, tld):
        """
        Sets the top-level domain.
        """
        self.domain = '.'.join(self.domain.split('.')[:1]) + '.' + tld

    @property
    def userinfo(self):
        """
        Retrieves the percent-encoded userinfo string, if one exists. 
        """
        if self._userinfo:
            return self.percent_encode(self._userinfo, regexes.USERINFO_REGEX)
        else:
            return None

    @userinfo.setter
    def userinfo(self, userinfo):
        """
        Set a new userinfo for this URI. 
        """
        if userinfo == "":
            userinfo = None
        self._userinfo = self.percent_decode(userinfo)

    def set_query_arg(self, key, value = None):
        """
        Sets a query argument. 
        """
        self.query_dict[key] = value

    def get_query_arg(self, key):
        """
        Gets a query argument.
        """
        return self.query_dict[key]

    @staticmethod
    def _is_ipv4(host_string):
        """
        Checks to see if a given host string is a valid IPv4 address
        """
        return regexes.IPV4_REGEX.search(host_string)

    @staticmethod
    def _is_ipvliteral(host_string):
        """
        Checks to see if a given host string is a valid IPvLiteral address
        """
        return regexes.IPVLITERAL_REGEX.search(host_string)

    @staticmethod
    def percent_encode(string, regex):
        """
        Percent-encode a string w/ hex codes.
        
        Given a provided string and regex, encodes any characters that don't 
        match the provided characters in the regex.

        Args:
            string: the string to be encoded
            regex: a regex listing any characters that don't need encoding
        """
        return ''.join(
            ['%' + x.encode('hex') if not regex.search(x) 
            else x for x in string])

    @staticmethod
    def percent_decode(string):
        """
        Percent-decode a string. See also: percent_encode(string, regex)
        """
        return ''.join(_PercentDecoder(string))
        
    def _build_authority(self, normalize = False):
        """
        Build a percent-encoded authority string and set the authority attribute.

        Takes the userinfo, host, and port attributes and attempts to build a 
        percent-encoded authority string. If the host is not set, returns None
        as a host is necessary for a valid authority string.
        """
        self._authority = ""
        if self._userinfo:
            self._authority += self.userinfo + '@'
        if self._host:
            if normalize:
                host = self.host.lower()
            else:
                host = self.host
        else:
            self.authority = None
            return
        self._authority += host
        if self.port:
            self._authority += ':' + str(self.port)

    def _build_query(self):
        """
        Build a percent-encoded query string from the query dict.
        """
        if len(self.query_dict.keys()) > 0:
            self._query = []
            for key, value in self.query_dict.iteritems():
                if value:
                    self._query.append(key + '=' + value)
                else:
                    self._query.append(key)
            self._query = '&'.join(self._query)
        else:
            self._query = None
    
    def _parse_authority(self):
        """
        Parses the authority attribute for userinfo, host, and port.

        Follows available regular expressesions to identify userinfo, host, 
        and port data. If identified, sets the corresponding attributes.
        If the host is of reg-name type (as opposed to IPv4 or an IP-literal),
        this function will also percent-decode the host.
        """
        if not self._authority:
            return
        auth_string = self._authority
        if auth_string.find('@') != -1:
            self.userinfo, auth_string = auth_string.split('@', 1)

        if self._is_ipv4(auth_string):
            search_result = self._is_ipv4(auth_string)
        elif self._is_ipvliteral(auth_string):
            search_result = self._is_ipvliteral(auth_string)
        else:
            search_result = regexes.REG_NAME_SEARCH_REGEX.search(auth_string)
        
        self.host = auth_string[search_result.start():search_result.end()]

        # Check for port info
        if len(auth_string) != len(self.host):
            self.port = auth_string[search_result.end() + 1:]

    def _parse_query(self):
        """
        Parse a query string into a query_dict attribute.
        """
        if self._query.find('&'):
            query_array = self._query.split('&')
        elif self._query.find(';'):
            query_array = self._query.split(';')
        else:
            query_array = [self._query]
        self.query_dict = {}
        for element in query_array:
            try:
                key, value = element.split('=')
                value = self.percent_decode(value)
            except ValueError:
                key, value = element, None
            key = self.percent_decode(key)
            self.query_dict[key] = value

    @staticmethod
    def _remove_dot_segments(path):
        """
        Removes dot segments from a given path.
        """
        segments = path.split('/')
        compressed_path = []
        for segment in segments:
            if segment == '.':
                pass
            elif segment == '..':
                compressed_path.pop()
            else:
                compressed_path.append(segment)
        return '/'.join(compressed_path)

    def chdir(self, changepath):
        """
        Functions like the UNIX cd or chdir command.

        Args
            changepath: the subdirectory to change to
        """
        if changepath[0] == '/':
            changepath = changepath[1:]
        if self._path[-1] == '':
            self._path.pop()
        self._path.extend(changepath.split('/'))

    @staticmethod
    def parse_uri(uri_string):
        """
        Parses a given URI using the regex provided in RFC 3986.
        """
        result = regexes.URI_REGEX.match(uri_string).groups()
        scheme, authority, path, query, fragment = \
                [result[i] for i in [1,3,4,6,8]]
        return URI(path = path, scheme = scheme, authority = authority, 
                query = query, fragment = fragment)

class _PercentDecoder(object):
    """
    Simple class implementing the iterable protocol for decoding a percent-
    encoded string. Generally implemented within other hidden functions.

    Standard usage would look as follows:

    decoded_string = ''.join(PercentDecoder(encoded_string))
    """
    def __init__(self, string):
        self.index = 0
        self.string = string

    def __iter__(self):
        return self

    def next(self):
        index = self.index
        if self.index >= len(self.string):
            raise StopIteration
        else:
            self.index += 1
            if self.string[index] == '%':
                self.index += 2
                return self.string[index+1:index+3].decode('hex')
            else:
                return self.string[index]


