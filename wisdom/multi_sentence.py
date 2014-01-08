#! coding:utf-8
import functools
from nltk import FreqDist
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from lesk import lesk
from utils import tokenize


ps = PorterStemmer()

def multi_sentence(context_sentences, ambiguous_word):
    fdist = FreqDist()
    for sentence in context_sentences:
        fdist.inc(lesk(sentence, ambiguous_word))
    return fdist.max()
