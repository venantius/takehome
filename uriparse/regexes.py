#!/usr/bin/env python
# encoding: utf-8

"""
This file consists of various regular expressions relevant to the parsing and 
interpretation of URIs. The core URI_REGEX is taken directly from the reference
RFC; others are borrowed from
http://jmrware.com/articles/2009/uri_regexp/URI_regex.html
"""

import re

# Used for the initial tokenization of the URI string; taken directly from 
# the RFC
URI_REGEX = re.compile(
        r'^(([^:/?#]+):)?(//([^/?#]*))?([^?#]*)(\?([^#]*))?(#(.*))?')

# Note that in general these only need to be defined for fields that will
# be percent-encoded. Keeping these "hidden" because they don't really need
# to be exposed
DEC_OCTET   = r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)'
UNRESERVED  = r'[A-Za-z0-9\-\.\_\~]'
GEN_DELIMS  = r'[\:\/\?\#\[\]\@]'
SUB_DELIMS  = r"[\!\$\&\'\(\)\*\+\,\;\=]"

# Authority regexes
USERINFO_REGEX = re.compile(r'|'.join([UNRESERVED, SUB_DELIMS, r'[\:]']))
IPV4_REGEX = re.compile(r'\.'.join([DEC_OCTET] * 4))
IPVLITERAL_REGEX = re.compile(r"(?:[[0-9A-Za-z\:]+])")
REG_NAME_SEARCH_REGEX = re.compile(r"(?:[A-Za-z0-9\-._~!$&'()*+,;=%])*")
REG_NAME_ELIGIBLE_REGEX = re.compile(r'|'.join([UNRESERVED, SUB_DELIMS]))

PCHAR = '|'.join([UNRESERVED, SUB_DELIMS, r'[\:\@]'])

# Path regexes
PATH_REGEX = re.compile(PCHAR)
PATH_NOSCHEME_REGEX = re.compile('|'.join([PCHAR, SUB_DELIMS, r'[\@]']))

# Just "allow" unreserved/sub-delims/:/@/, functions will pct-encode
# everything else
QUERY_REGEX = re.compile('|'.join([PCHAR, r'[\/\?]']))
FRAGMENT_REGEX = re.compile('|'.join([PCHAR, r'[\/\?]']))


