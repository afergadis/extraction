__author__ = 'Aris Fergadis'
__version__ = 0.1

import logging
import sys
from operator import itemgetter

import nltk
from gensim import corpora, models

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

if len(sys.argv) != 3:
    print "Usage: extract document_name extraction_percent"
    print "\tExample: extract sleep.txt 10"
    exit(1)

# Read article
f = open(sys.argv[1])
article = f.read()
f.close()

# Sentence segmentation and tokenization
document_orig = nltk.sent_tokenize(article)
document = [nltk.word_tokenize(line) for line in document_orig]

# Remove stop words and punctuation
stopwords = open('stopwords/english').read().splitlines()
punctuation = ['.', ',', ';', ':', '!', '?', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '-', "'"]
stoplist = stopwords + punctuation
sentences = [[word.lower() for word in sentence
              if word.lower() not in stoplist]
             for sentence in document]

# Remove words that appears only once
all_tokens = sum(sentences, [])
tokens_once = set(word for word in set(all_tokens) if all_tokens.count(word) == 1)
sentences = [[word for word in text if word not in tokens_once]
             for text in sentences]

# Assign a unique integer id to all words appearing in the document
dictionary = corpora.Dictionary(sentences)

# The function doc2bow() simply counts the number of occurrences of each
# distinct word, converts the word to its integer word id and returns the
# result as a sparse vector.
corpus = [dictionary.doc2bow(sent) for sent in sentences]

# Initialize the tfidf model
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
extract_len = int(round(len(sentences) * (int(sys.argv[2])) / 100.0))

# Sort sentences by score in descending order
sorted_sents_by_score = sorted(sentences_score, key=itemgetter(1), reverse=True)
# Sort hi score sentences by sentence number as the appear in document
hi_score_sents = sorted(sorted_sents_by_score[:extract_len], key=itemgetter(0))

# Some statistics
print "Document sentences: {0}".format(len(sentences))
print "Extraction sentences: {0}\n".format(extract_len)

#print document_orig[0]  # print title
for sent in hi_score_sents:
    sent_id, _ = sent
    print document_orig[sent_id]