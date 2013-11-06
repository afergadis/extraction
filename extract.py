__author__ = 'Aris Fergadis'
__version__ = 0.1

import codecs
import logging
import sys

from operator import itemgetter
from preprocess import Preprocess
from gensim import corpora, models

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


def sentences_length(sentences):
    """
    Returns the shortest and longest acceptable sentences sentences length

    The shortest is 50% less of the average sentence length and the longest 50% more
    """
    summary = 0
    for s in sentences:
        summary += len(s)
    avg = 1.0 * summary / len(sentences)
    long_len = int(avg * 1.5)
    return long_len


if len(sys.argv) != 3:
    file_to_open = raw_input("File to open: ")
    summary_len = raw_input("Extraction length in percent (without %): ")
else:
    file_to_open = sys.argv[1]
    summary_len = sys.argv[2]

# Read article
f = codecs.open(file_to_open, encoding='utf-8')
article = f.read()
f.close()

# Preprocess article
ppd = Preprocess(article)
sentences = ppd.sentences
dictionary_text = ppd.dictionary_text

# Assign a unique integer id to all words appearing in the document
dictionary = corpora.Dictionary(dictionary_text)

# The function doc2bow() simply counts the number of occurrences of each
# distinct word, converts the word to its integer word id and returns the
# result as a sparse vector.
corpus = [dictionary.doc2bow(sent) for sent in dictionary_text]

# Initialize the tfidf model
tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]

# Remove paragraphs that are too short_len or too long_len
long_len = sentences_length(sentences)
sents_2_remove = []
for sent_id, sent in enumerate(sentences):
    sent_len = len(sent)
    if sent_len > long_len:
        sents_2_remove.append(sent_id)

# Calculate the sentences' score
sentences_score = []
for sent_id, doc in enumerate(corpus_tfidf):
    sent_score = 0
    if sent_id in sents_2_remove:
        continue
    for term_id, term_score in doc:
        sent_score += term_score
    sentences_score.append((sent_id, sent_score))

# "Summary" length
extract_len = int(round(len(sentences) * (int(summary_len)) / 100.0))

# Sort sentences by score in descending order
sorted_sents_by_score = sorted(sentences_score, key=itemgetter(1), reverse=True)
# Sort hi score sentences by sentence number as the appear in document_words
hi_score_sents = sorted(sorted_sents_by_score[:extract_len], key=itemgetter(0))

# Some statistics
print "Document sentences: {0}".format(len(sentences))
print "Extraction sentences: {0}\n".format(int(round(len(sentences) * (int(summary_len)) / 100.0)))
#print document_sents[0]  # print title
for sent in hi_score_sents:
    sent_id, _ = sent
    print sentences[sent_id]