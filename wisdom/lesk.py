#! coding:utf-8
import functools
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from utils import tokenize


ps = PorterStemmer()
english_stopwords = stopwords.words('english')

def __build_dictionary(synset, hyperhypo):
    lesk_dictionary = []
    # Includes definition.
    lesk_dictionary+= tokenize(synset.definition)
    # Includes lemma_names.
    lesk_dictionary+= synset.lemma_names
    # Optional: includes lemma_names of hypernyms and hyponyms.
    if hyperhypo:
        related_senses = synset.hypernyms()+synset.hyponyms()
        lesk_dictionary+= [lemma.name for related_synset in related_senses for lemma in related_synset.lemmas ]       

    return filter(lambda word: word not in english_stopwords, lesk_dictionary)


def base_lesk(context_sentence, ambiguous_word, pos, stem, build_dictionary_function):
    max_overlaps = 0
    lesk_sense = None
    
    context_sentence = tokenize(context_sentence)
    for ss in wn.synsets(ambiguous_word):
        if pos and ss.pos != pos:
            continue

        lesk_dictionary = build_dictionary_function(ss)
        # Matching exact words causes sparsity, so lets match stems.
        if stem:
            lesk_dictionary = [ps.stem(i) for i in lesk_dictionary]
            context_sentence = [ps.stem(i) for i in context_sentence] 

        overlaps = set(lesk_dictionary).intersection(context_sentence)

        if len(overlaps) > max_overlaps:
            lesk_sense = ss
            max_overlaps = len(overlaps)
    return lesk_sense




def lesk(context_sentence, ambiguous_word, pos=None, stem=True, hyperhypo=True):
    return base_lesk(context_sentence, 
        ambiguous_word, 
        pos, 
        stem, 
        functools.partial(__build_dictionary, hyperhypo=hyperhypo))
