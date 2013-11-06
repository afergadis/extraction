__author__ = 'aris'
__version__ = 0.1
__date__ = '11/5/13'

import csv
import enchant
import yaml
from nltk.metrics import edit_distance


class SpellingReplacer(object):
    """ Corrects minor spelling issues using Enchant  - a spelling correction API

        Create an instance giving the language dictionary
        and the maximum number of different characters
        between word and dictionary's suggestion.

        Available languages depend on your installation.

        Example of use:
            >>> from replacers import SpellingReplacer
            >>> replacer = SpellingReplacer()
            >>> replacer.replace('cookbok')
            'cookbook'
    """

    def __init__(self, dict_name='en', max_dist=2):
        self.spell_dict = enchant.Dict(dict_name)
        self.max_dist = max_dist

    def replace(self, word):
        if self.spell_dict.check(word):  # If the word is in the dictionary, the it is correct
            return word  # return in
        suggestions = self.spell_dict.suggest(word)  # Ge a suggestion list
        if suggestions and edit_distance(word, suggestions[0]) <= self.max_dist:
            # If word and 1st suggestion has maximum max_dist different characters
            return suggestions[0]  # return 1st suggestion
        else:
            return word  # return original word


class CustomSpellingReplacer(SpellingReplacer):
    def __init__(self, dict_name='en', custom_dict='custom_dict.txt', max_dist=2):
        self.spell_dict = enchant.DictWithPWL(dict_name, custom_dict)
        self.max_dist = max_dist


class WordReplacer(object):
    """ WordReplacer is simply a class wrapper around a Python dictionary.

        The replace() method looks up the given word in its word_map and returns
        the replacement synonym if it exists. Otherwise, the given word is returned as is.

        WordReplacer can act as a base class for other classes that construct the
        word_map from various file formats.
    """

    def __init__(self, word_map):
        self.word_map = word_map

    def replace(self, word):
        return self.word_map.get(word, word)


class CsvWordReplacer(WordReplacer):
    """ Fills a word map dictionary with pairs (word, synonym) found in a csv file.

        The pairs are comma separated
        bday, birthday
    """

    def __init__(self, fname):
        word_map = {}
        for line in csv.reader(open(fname)):
            word, syn = line
            word_map[word] = syn
        super(CSVWordReplacer, self).__init__(word_map)


class YamlWordReplacer(WordReplacer):
    """ Fills a word map dictionary with pairs (word: synonym) found in a yaml file.

        The pairs are colon separated
        bday: birthday
    """

    def __init__(self, fname):
        word_map = yaml.load(open(fname))
        super(YamlWordReplacer, self).__init__(word_map)