#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils.file_operations import *
from objects.page import *

class Classifier(object):
    """
    """
    
    def __init__(self):
        """
        """
        word_list = FileOperations.get_word_list()
        for word in word_list:
            synset_list = FileOperations.get_synset_list(word)
            rooted_list = FileOperations.get_root_words(word)
            page_list = self.line_list_to_page_object(rooted_list)

            
    def line_list_to_page_object(line_list):
        """
        """
        



if __name__ == '__main__':
    classifier = Classifier()
        
        

