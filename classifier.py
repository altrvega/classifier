#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils.file_operations import *
from utils.translator import *
from utils.wordnet import *
from objects.page import *
from nltk.corpus import wordnet as wn

class Classifier(object):
    """
    """
    
    def __init__(self):
        """
        """
        word_list = FileOperations.get_word_list()
        for word in word_list:
            word = word.strip()
            synset_list = FileOperations.get_synset_list(word)
            synset_list = self.convert_synset_dict(synset_list)
            rooted_list = FileOperations.read_rooted_words(word)
            page_list = self.line_list_to_page_object(rooted_list)
            for page in page_list:
                page_class = self.classify(word, page, synset_list)
                print page._link +  '   '  + str(page_class)


    def convert_synset_dict(self, synset_list):
        """
        """
        dict = {}
        for syn_line in synset_list:
            syn_info = syn_line.split(':', 1)
            syn_info = syn_info[0]
            syn_info = syn_info.split(' ', 1)
            idx = syn_info[0]
            synset = wn.synset(syn_info[1])
            near_synsets = self.get_near_synsets(synset)
            dict[idx] = near_synsets
        return dict

    def get_near_synsets(self, synset):
        """2 based hypernym
        """
        all_hypernyms = []
        hypernyms = synset.hypernyms()
        for hype in hypernyms:
            sec_hypernyms = hype.hypernyms()
            hypernyms = hypernyms + sec_hypernyms
        hyponyms = synset.hyponyms()
        holonyms = synset.member_holonyms()
        all_near_synsets = hypernyms + hyponyms + holonyms
        return all_near_synsets

            
    def line_list_to_page_object(self, line_list):
        """
        """
        obj_list = []
        for line in line_list:
            page_info = line.split(' ', 1)
            link = page_info[0]
            text = page_info[1]
            page = Page(link, None, None)
            text = text.strip()
            page._words = text.split(' ')
            obj_list.append(page)
        return obj_list

    def classify(self, keyword,  page, synset_list):
        """
        """
        points = self.initialize_points(synset_list)
        for word in page._words:
            if (word == keyword):
                continue
            meaning_list = self.get_meanings(word)
            page_word_synsets = []
            for mean in meaning_list:
                temp_list = WordnetProcess.getSynsets(mean, pos='NOUN', limit=3)
                for synset in temp_list:
                    if (synset not in page_word_synsets):
                        page_word_synsets.append(synset)
            set_page_word_synsets = set(page_word_synsets)
            page_word_hypernyms = self.get_all_hypernyms(page_word_synsets)
            set_page_word_hypernyms = set(page_word_hypernyms)
            page_word_hyponyms = self.get_all_hyponyms(page_word_synsets)
            set_page_word_hyponyms = set(page_word_hyponyms)
            page_word_holonyms = self.get_all_holonyms(page_word_synsets)
            set_page_word_holonyms = set(page_word_holonyms)
            for syn_idx in synset_list:
                sub_synsets = synset_list[syn_idx]
                set_sub_synsets = set(sub_synsets)
                if (set_sub_synsets.intersection(set_page_word_synsets)):
                    points[syn_idx] = points[syn_idx] + 1
                    break
                if (set_sub_synsets.intersection(set_page_word_hypernyms)):
                    points[syn_idx] = points[syn_idx] + 1
                    break
                if (set_sub_synsets.intersection(set_page_word_hyponyms)):
                    points[syn_idx] = points[syn_idx] + 1
                    break
                if (set_sub_synsets.intersection(set_page_word_holonyms)):
                    points[syn_idx] = points[syn_idx] + 1
                    break
        #print page._link
        #print points
        #print keyword
        return self.get_biggest_value(points)

    def get_biggest_value(self, dict):
        biggest_val = 0
        biggest_idx = 0
        for key in dict:
            if (dict[key] > biggest_val):
                biggest_val = dict[key]
                biggest_idx = key
        return biggest_idx

    def get_meanings(self, word):
        trObj = Translator(word)
        trObj.create_meaning_list()
        meaning_list = trObj.englishMeanings
        if (len(meaning_list) > 2):
            meaning_list = meaning_list[0:2]
        return meaning_list

    def get_all_hyponyms(self, synset_list):
        """
        """
        all_hyponyms = []
        for synset in synset_list:
            hyponyms = synset.hyponyms()
            for hypo in hyponyms:
                if (hypo not in all_hyponyms):
                    all_hyponyms.append(hypo)
        return all_hyponyms

    
    def get_all_hypernyms(self, synset_list):
        """
        """
        all_hypernyms = []
        for synset in synset_list:
            hypernyms = synset.hypernyms()
            for hype in hypernyms:
                if (hype not in all_hypernyms):
                    all_hypernyms.append(hype)

        #hypernyms of hypernyms
        sec_hypernyms = []
        for synset in all_hypernyms:
            hypernyms = synset.hypernyms()
            for hype in hypernyms:
                if (hype not in sec_hypernyms):
                    sec_hypernyms.append(hype)
        all_hypernyms = all_hypernyms + sec_hypernyms
        return all_hypernyms

    def get_all_holonyms(self, synset_list):
        """
        """
        all_holonyms = []
        for synset in synset_list:
            holonyms = synset.member_holonyms()
            for holo in holonyms:
                if (holo not in all_holonyms):
                    all_holonyms.append(holo)
        return all_holonyms

    def initialize_points(self, synset_list):
        points = {}
        for key in synset_list:
            points[key] = 0
        return points


if __name__ == '__main__':
    classifier = Classifier()
        
        

