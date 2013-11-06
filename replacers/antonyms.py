"""
Module docstring
"""

__author__ = "Aris Fergadis"
__version__ = "$Revision: 1.0 $"
__date__ = "Aug 30, 2013"
__copyright__ = "Copyright (c) ..."
__license__ = "Python"

from nltk.corpus import wordnet
from synonyms import WordReplacer


class AntonymReplacer(object):
    """
    With antonym replacement, you can replace "not uglify" with "beautify",
    in sentence "let's not unglify our code" resulting in the sentence
    "let's beautify our code".
    
    Example of use:
        >>> from replacers.antonyms import AntonymReplacer
        >>> replacer = AntonymReplacer()
        >>> replacer.replace('good')
        >>> replacer.replace('uglify')
        'beautify'
        >>> sent = ["let's", 'not', 'uglify', 'our', 'code']
        >>> replacer.replace_negations(sent)
        ["let's", 'beautify', 'our', 'code']
    """

    def replace(self, word, pos=None):
        """
        The method takes a single word and an optional part of speech tag, then looks up
        the synsets for the word in WordNet. Going through all the synsets and every lemma of each
        synset, it creates a set of all antonyms found. If only one antonym is found, then it is an
        unambiguous replacement. If there is more than one antonym found, which can happen quite
        often, then we don't know for sure which antonym is correct. In the case of multiple antonyms
        (or no antonyms), replace() returns None since it cannot make a decision.
        
        :param word: the word to search for it's antonym
        :type word: C{str}
        :param pos: part of speech, one of 'v', 'n', 'r', 'a'
        :type pos: C{str}
        """
        antonyms = set()
        for syn in wordnet.synsets(word, pos=pos):
            for lemma in syn.lemmas:
                for antonym in lemma.antonyms():
                    antonyms.add(antonym.name)
                    if len(antonyms) == 1:
                        return antonyms.pop()
                    else:
                        return None
                    
    def replace_negations(self, sent):
        """
        The method looks through a tokenized sentence for the word "not". If "not" is found,
        then we try to find an antonym for the next word using replace(). If we find an antonym,
        then it is appended to the list of words, replacing "not" and the original word.
        All other words are appended as it is, resulting in a tokenized sentence with unambiguous
        negations replaced by their antonyms.
        
        :param sent: the sentence in which the replacement takes place
        :type sent: list of strings
        """
        i, l = 0, len(sent)
        words = []
        while i < l:
            word = sent[i]
            if word == 'not' and i + 1 < l:
                ant = self.replace(sent[i + 1])
                if ant:
                    words.append(ant)
                    i += 2
                    continue
            words.append(word)
            i += 1
        return words


# The order of inheritance is very important, as we want the initialization and replace()
# function of WordReplacer combined with the replace_negations() function from
# AntonymReplacer.
class AntonymWordReplacer(WordReplacer, AntonymReplacer):
    """
    Since unambiguous antonyms aren't very common in WordNet, we may want to create a
    custom antonym mapping the same way we did for synonyms. This AntonymWordReplacer
    is constructed by inheriting from both WordReplacer and AntonymReplacer.
    
    Example of use:
        >>> from replacers.antonyms import AntonymWordReplacer
        >>> replacer = AntonymWordReplacer({'evil': 'good'})
        >>> replacer.replace_negations(['good', 'is', 'not', 'evil'])
        ['good', 'is', 'good']
    """
    pass
