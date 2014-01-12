#! coding:utf-8
import functools
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from utils import tokenize
from exceptions import NoSenseFound
from collections import Counter

ps = PorterStemmer()
wnl = WordNetLemmatizer()

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
        for related_sense in related_senses:
            lesk_dictionary+= tokenize(related_sense.definition)
            lesk_dictionary+= [lemma.name for lemma in related_sense.lemmas]

    return filter(lambda word: word not in english_stopwords, lesk_dictionary)

def compute_overlap(context_sentence, synset, stem, build_dictionary_function):
    word_gloss = build_dictionary_function(synset)
    # Matching exact words causes sparsity, so lets match stems.
    if stem:
        word_gloss = [ps.stem(i) for i in word_gloss]
        context_sentence = [ps.stem(i) for i in context_sentence] 

    # Now, lets count the words in dictionary 
    gloss_counter = Counter(word_gloss)
    sentence_counter = Counter(context_sentence)

    intersection = gloss_counter & sentence_counter

    return sum(intersection.itervalues())

def base_lesk(context_sentence, ambiguous_word, pos, stem, build_dictionary_function):
    context_sentence = tokenize(context_sentence)
    if ambiguous_word not in context_sentence:
        raise NoSenseFound("Word not found in sentence")

    overlaps = {}
    synsets = wn.synsets(ambiguous_word)

    if len(synsets) == 0:
        raise NoSenseFound("Word has no possible senses")

    for synset in wn.synsets(ambiguous_word):
        if pos and synset.pos != pos:
            continue
        overlaps[synset] = compute_overlap(context_sentence, synset, stem, build_dictionary_function)
    
    best_synset, max_overlaps = max(overlaps.iteritems(), key=lambda (synset, overlaps): overlaps)
    if max_overlaps == 0 :
        raise NoSenseFound()
    return best_synset




def lesk(context_sentence, ambiguous_word, pos=None, stem=True, hyperhypo=True):
    return base_lesk(context_sentence, 
        ambiguous_word, 
        pos, 
        stem, 
        functools.partial(__build_dictionary, hyperhypo=hyperhypo))
