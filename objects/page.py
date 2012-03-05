#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Page(object):
    """holds page information
    """
    
    def __init__(self, link, title, snippet):
        """
        
        Arguments:
        - `link`: link of the page
        - `title`:title of the page
        - `text`: text of the page
        - `snippet`: snippet of the page
        """
        self._link = link
        self._title = title
        self._snippet = snippet
        self._words = []
        if (title and snippet):
            self._text = title + snippet
        else:
            self._text = ""
        
        
