import re


class RegexpReplacerTypeError(Exception):
    pass


class RegexpReplacer(object):
    """
    RegexpReplacer replaces every instance of a replacement pattern
    with its corresponding substitution pattern.
    
    Example of use:
        >>> from replacers.regexp import RegexpReplacer
        >>> replacer = RegexpReplacer()
        >>> replacer.replace("can't is a contraction")
        'cannot is a contraction'
        >>> replacer.replace("I should've done that thing I didn't do")
        'I should have done that thing I did not do'
        
    You can use your own replacement patterns in the form of:
        my_replacement_patterns = [
            (r'won\'t', 'will not'),
            (r'can\'t', 'cannot'),
            (r'(\w+)\'ll', '\g<1> will')]
    in the creation of RegexpReplacer object.
    Example of use:
        >>> replacer = RegexpReplacer(my_replacement_patters)
    """

    def __init__(self, language='en'):
        self.patterns = []
        for rule in open('regexp_rules.%s' % language):
            regexp, repl = rule.split(' ', 1)  # split on 1st space
            #self.patterns.append((re.compile(regexp), repl.strip()))
            self.patterns.append((regexp, repl.strip()))

    def replace(self, text):
        """
        Replaces every instance of a replacement search_pattern 
        with its corresponding substitution.
        """
        if isinstance(text, str):
            s = text
            for (search_pattern, repl) in self.patterns:
                (s, _) = re.subn(search_pattern, repl, s)
            return s
        elif isinstance(text, list):
            l = []
            for s in text:
                for (search_pattern, repl) in self.patterns:
                    try:
                        (s, _) = re.subn(search_pattern, repl, s)
                    except TypeError:
                        raise (RegexpReplacerTypeError, "A list of string objects expected.")
                l.append(s)
            return l
        else:
            raise (RegexpReplacerTypeError, "Argument should be string or list of strings")


if __name__ == "__main__":
    replacer = RegexpReplacer()
    print replacer.replace("can't is a contraction")
    print replacer.replace("I should've done that thing I didn't do")