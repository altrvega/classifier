#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os
from properties.properties import *


class FileOperations(object):
    """File Operations utility
    """

    @staticmethod
    def get_file_list(*args):
        """returns the name of files
        in the given directory
        """
        if args:
            dir = args[0]
        else:
            dir = properties['file_dir']
        file_list = os.listdir(dir)
        return file_list
        
    @staticmethod
    def get_word_list():
        """get word list from file
        """
        file_path = properties['file_dir'] + 'words.txt'
        f = io.open(file_path, 'r')
        word_list = f.readlines()
        f.close()
        return word_list

    @staticmethod
    def get_synset_list(word):
        """
        """
        word = word.strip()
        file_path = properties['synsets_dir'] + word + '.txt'
        f = io.open(file_path, 'r')
        synset_list = f.readlines()
        f.close()
        return synset_list

    @staticmethod
    def read_rooted_words(word):
        word = word.strip()
        file_path = properties['roots_dir'] + word + '.txt'
        f = io.open(file_path, 'r')
        line_list = f.readlines()
        f.close()
        return line_list


    @staticmethod
    def write_list_to_file(list_obj, word):
        f = io.open(properties['output_dir'] + word.encode('utf-8') + '.txt', 'a')
        for obj in list_obj:
            obj = obj + '\n'
            obj = unicode(obj)
            f.write(obj)
        f.close()


    @staticmethod
    def read_file_lines_to_list(*args):
        """firt argument for filename
        second argument for path (if not read from property
        """
        file_name = args[0]
        if (len(args) == 2):
            file_path = args[1]
        else:
            file_path = properties['file_dir']
        f = io.open(file_path + file_name, 'r')
        file_text = f.readlines()
        f.close()
        return file_text
        
        

    @staticmethod
    def write_word_results(object_list):
        """write page information to a file
        not using in here
        """
        file_name = properties['search_word']
        f = io.open(properties['output_dir'] + file_name.encode('utf-8') + '.txt', 'a')
        for obj in object_list:
            line = obj._link + ' ' + obj._title + ' ' + obj._snippet + '\n'
            f.write(line)
        f.close()

    @staticmethod
    def write_rooted_words(object_list, word):
        """
        """
        f = io.open(properties['output_dir'] + word + '.txt', 'w')
        for obj in object_list:
            text = ''
            for word in obj._words:
                text = text + ' ' + word
            line = obj._link + ' ' + text + '\n'
            f.write(line)
        f.close()
        
        
        

        
        
