"""
It is often useful to reduce the vocabulary of a text by replacing words with common
synonyms. By compressing the vocabulary without losing meaning, you can save memory in
cases such as frequency analysis and text indexing. Vocabulary reduction can also increase
the occurrence of significant collocations.
"""

__author__ = "Aris Fergadis"
__version__ = "$Revision: 1.0 $"
__date__ = "30/12/2013"
__copyright__ = "Copyright (c) ..."
__license__ = "Python"

import csv
import yaml


class WordReplacerWrongDict(Exception):
    pass


class WordReplacer(object):
    """
    WordReplacer is simply a class wrapper around a Python dictionary. The replace()
    method looks up the given word in its word_map and returns the replacement synonym
    if it exists. Otherwise, the given word is returned as is.
    
    Example of use:
        >>> from replacers.synonyms import wordReplacer
        >>> replacer = WordReplacer({'bday': 'birthday'})
        >>> replacer.replace('bday')
        'birthday'
        >>> replacer.replace('happy')
        'happy'
    """
    def __init__(self, word_map):
        if not isinstance(word_map, dict):
            raise(WordReplacerWrongDict, "Initialize with a dictionary of words {'key': 'value'}")
        
        self.word_map = word_map

    def replace(self, word):
        return self.word_map.get(word, word)


class CsvWordReplacer(WordReplacer):
    """
    CsvWordReplacer uses a csv file to make word replacements.
    Csv file format is as follows:
        bday, birthday
        tue, Tuesday
        
    Example of use:
        >>> from replacers.synonyms import CsvWordReplacer
        >>> replacer = CsvWordReplacer('synonyms.csv')
        >>> replacer.replace('bday')
        'birthday'
        >>> replacer.replace('happy')
        'happy'
    """
    def __init__(self, fname):
        word_map = {}
        for line in csv.reader(open(fname)):
            word, syn = line
            word_map[word] = syn
            super(CsvWordReplacer, self).__init__(word_map)


class YamlWordReplacer(WordReplacer):
    """
    YamlWordReplacer uses a yaml file to make word replacements.
    Yaml file format is as follows:
        bday: birthday
        tue: Tuesday
        
    Example of use:
        >>> from replacers.synonyms import YamlWordReplacer
        >>> replacer = YamlWordReplacer('synonyms.yaml')
        >>> replacer.replace('bday')
        'birthday'
        >>> replacer.replace('happy')
        'happy'
    """
    
    def __init__(self, fname):
        word_map = yaml.load(open(fname))
        super(YamlWordReplacer, self).__init__(word_map)
