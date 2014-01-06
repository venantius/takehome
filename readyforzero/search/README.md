rfz-search
==========

An efficient full text search engine written for Ready For Zero 

A server that does efficient instant full text search (e.g.: POST "Alabama" to /add endpoint, then GET "aba" on /search would return "Alabama")

 - search1: Do this in constant (O(1)) time without searching the list.
 - search2: What if you needed to be able to find "with corrections", eg: "aban" return "Alabama"?
 - search3: What if you just had to indicate if there are any search results?

Requirements
------------
 - Tornado

Extras
------
 - search2\_suffixarray -- does fuzzy text searching using a suffix array implementation based on one of the algorithms referenced [here](http://www.cs.umd.edu/grad/scholarlypapers/papers/ghodsi.pdf)

Todo
----
 - Update search3 to use golomb/rice codes
