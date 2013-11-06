import re
from nltk.corpus import wordnet
 
 
class RepeatReplacer(object):
    """
    In everyday language, people are often not strictly grammatical. They will write things like
    "I looooooove it" in order to emphasize the word "love". But computers don't know that
    "looooooove" is a variation of "love" unless they are told. This replacer is a method for
    removing those annoying repeating characters in order to end up with a "proper" English word.
    
    Example of use:
        >>> from replacers.repeat import RepeatReplacer
        >>> replacer = RepeatReplacer()
        >>> replacer.replace('looooove')
        'love'
        >>> replacer.replace('oooooh')
        'ooh'
        >>> replacer.replace('goose')
        'goose'
    """

    def __init__(self):
        """
        Initialize the repeat and replacement patterns used for substitution.  
        """
        self._repeat_pattern = r'(\w*)(\w)\2(\w*)'
        # Zero or more starting characters
        # A single character (\w), followed by another instance of that character \2.
        # Zero or more ending characters
        self._repeat_regexp = re.compile(self._repeat_pattern)
        self._repl = r'\1\2\3'
        
    def replace(self, word):
        """
        Replaces repeated characters in a given word. E.g. "looooove" becomes "love"
        """
        if wordnet.synsets(word):
            return word
        repl_word = self._repeat_regexp.sub(self._repl, word)
        if repl_word != word:
            return self.replace(repl_word)
        else:
            return repl_word
