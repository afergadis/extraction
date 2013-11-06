__author__ = 'aris'
__version__ = 0.1
__date__ = '11/3/13'

# Tokenize
# Tag
# Chunk
# Collocations?
# Untag
# Stemm
# Wordnet (synonyms)

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tag import pos_tag
from nltk.stem import PorterStemmer
from nltk.collocations import BigramAssocMeasures, BigramCollocationFinder


class Preprocess():
    def __init__(self, document):
        self.text = document  # Original text
        self.sentences = self.split_sentences(self.text)  # Original text tokenized in sentences
        self.words = self.split_words(self.sentences)
        self.pos_text = self.tag(self.words)  # Original text with POS tagged words
        # TODO chunk
        self._clean_text = self.clean(self.words)  # Remove stop words and punctuation
        self._stemmed_text = self.stem(self._clean_text)  # Word stemming
        self.dictionary_text = self._stemmed_text  # Find collocations

    def strip(self, sentence, start_token='(', end_token=')'):
        while True:
            start = sentence.find(start_token)  # Find opening parenthesis
            if start < 0:  # If there is not any
                break  # break loop and go to next sentence
            end = sentence.find(end_token) + 1  # Find closing parenthesis
            if end < 0:  # If not found (?)
                break  # break loop and go to next sentence
            sentence = sentence[:start] + sentence[end:]  #
        return sentence

    def split_sentences(self, text):
        sentences = sent_tokenize(text)

        # Remove sentences in parenthesis
        stripped_sentences = [self.strip(sentence, start_token='(', end_token=')')
                              for sentence in sentences]
        # Remove sentences in []
        stripped_sentences = [self.strip(sentence, start_token='(', end_token=')')
                              for sentence in stripped_sentences]

        return stripped_sentences

    def split_words(self, text):
        return [word_tokenize(sentence) for sentence in text]

    def tag(self, text):
        return [pos_tag(token) for token in text]

    def chunk(self, text):
        grammar = r'''QUOTE : {<:><.*>*<:>}  # quotation followed by any tags and clossing quotation'''
        return text

    def collocations(self, text):
        flatten_text = [word for sentence in text for word in sentence]
        bcf = BigramCollocationFinder.from_words(flatten_text)
        clist = bcf.nbest(BigramAssocMeasures.likelihood_ratio, 4)

        t = []
        for sentence in text:
            s = []
            for word in sentence:  # TODO FIX: appends collocation's 2nd word two times
                used = False
                for pair in clist:
                    if word == pair[0]:
                        s.append(pair[0] + " " + pair[1])
                        used = True
                        break
                if not used:
                    s.append(word)
            t.append(s)

        return t

    def clean(self, text):
        stopwords = open('stopwords/english').read().splitlines()
        punctuation = ['.', ',', ';', ':', '!', '?', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '-', "'"]
        stoplist = stopwords + punctuation

        stopfree_text = [[word.lower() for word in sentence if word.lower() not in stoplist]
                         for sentence in text]

        return stopfree_text

    def stem(self, text):
        clean_text = self.clean(text)
        stemmer = PorterStemmer()
        tokens = [[stemmer.stem(word) for word in sentence] for sentence in clean_text]

        # Remove tokens that appears only once
        all_tokens = sum(tokens, [])
        tokens_once = set(token for token in set(all_tokens) if all_tokens.count(token) == 1)
        tokens = [[token for token in sentence if token not in tokens_once]
                  for sentence in tokens]

        return tokens


if __name__ == "__main__":
    from operator import itemgetter
    from gensim import corpora, models

    summary_len = 10
    #text = open("../extraction/Sleep").read()
    text = """The top portion has a metal staple (mel anaichu) into which is inserted a small
    metallic cylinder (kendai) which carries the mouthpiece made of reed. Besides spare reeds,
    a small ivory or horn needle is attached to the instrument, and used to clear the reed of
    saliva and other debris and allows free passage of air. A metallic bell (keezh anaichu)
    forms the bottom end of the instrument.
    """
    pd = Preprocess(text)
    document = pd.sentences  # Original text tokenized in sentences
    dict_text = pd.preprocessed_text

    dictionary = corpora.Dictionary(dict_text)
    corpus = [dictionary.doc2bow(s) for s in dict_text]

    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]

    # Calculate the sentences' score
    sentences_score = []
    for sent_id, doc in enumerate(corpus_tfidf):
        sent_score = 0
        for term_id, term_score in doc:
            sent_score += term_score
        sentences_score.append((sent_id, sent_score))

    # "Summary" length
    extract_len = int(round(len(document) * (int(summary_len)) / 100.0))

    # Sort sentences by score in descending order
    sorted_sents_by_score = sorted(sentences_score, key=itemgetter(1), reverse=True)
    # Sort hi score sentences by sentence number as the appear in document_words
    hi_score_sents = sorted(sorted_sents_by_score[:extract_len], key=itemgetter(0))

    # Some statistics
    print "Document sentences: {0}".format(len(document))
    print "Extraction sentences: {0}\n".format(int(round(len(document) * (int(summary_len)) / 100.0)))
    #print document_sents[0]  # print title
    for sent in hi_score_sents:
        sent_id, _ = sent
        print document[sent_id]