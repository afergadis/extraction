import enchant
from nltk.metrics import edit_distance

class SpellingReplacer(object):
    """
    Corrects minor spelling issues using Enchant - a spelling correction API
    
    Example of use:
        >>> from replacers.spelling import SpellingReplacer
        >>> replacer = SpellingReplacer()
        >>> replacer.replace('cookbok')
        'cookbook'
    """


    def __init__(self, dict_name='en', max_dist=2):
        self.spell_dict = enchant.Dict(dict_name)
        self.max_dist = max_dist
        
    def replace(self, word):
        if self.spell_dict.check(word):
            return word
        suggestions = self.spell_dict.suggest(word)
        if suggestions and edit_distance(word, suggestions[0]) <= self.max_dist:
            return suggestions[0]
        else:
            return word
        
class CustomSpellingReplacer(SpellingReplacer):
    
    def __init__(self, dict_name='en', custom_dict='custom_dict.txt', max_dist=2):
        self.spell_dict = enchant.DictWithPWL(dict_name, custom_dict)
        self.max_dist = max_dist
        
