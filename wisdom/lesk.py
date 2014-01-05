from nltk.corpus import wordnet as wn
from nltk.stem import PorterStemmer
from itertools import chain

bank_sents = ['I went to the bank to deposit my money',
'The river bank was full of dead fishes']

plant_sents = ['The workers at the industrial plant were overworked',
'The plant was no longer bearing flowers']

ps = PorterStemmer()

def lesk(context_sentence, ambiguous_word, pos=None, stem=True, hyperhypo=True):
    max_overlaps = 0; lesk_sense = None
    context_sentence = context_sentence.split()
    for ss in wn.synsets(ambiguous_word):
        # If POS is specified.
        if pos and ss.pos is not pos:
            continue

        lesk_dictionary = []

        # Includes definition.
        lesk_dictionary+= ss.definition.split()
        # Includes lemma_names.
        lesk_dictionary+= ss.lemma_names

        # Optional: includes lemma_names of hypernyms and hyponyms.
        if hyperhypo == True:
            lesk_dictionary+= list(chain(*[i.lemma_names for i in ss.hypernyms()+ss.hyponyms()]))       

        if stem == True: # Matching exact words causes sparsity, so lets match stems.
            lesk_dictionary = [ps.stem(i) for i in lesk_dictionary]
            context_sentence = [ps.stem(i) for i in context_sentence] 

        overlaps = set(lesk_dictionary).intersection(context_sentence)

        if len(overlaps) > max_overlaps:
            lesk_sense = ss
            max_overlaps = len(overlaps)
    return lesk_sense

# print "Context:", bank_sents[0]
# answer = lesk(bank_sents[0],'bank')
# print "Sense:", answer
# print "Definition:",answer.definition
# print

# print "Context:", bank_sents[1]
# answer = lesk(bank_sents[1],'bank','n')
# print "Sense:", answer
# print "Definition:",answer.definition
# print

# print "Context:", plant_sents[0]
# answer = lesk(plant_sents[0],'plant','n', True)
# print "Sense:", answer
# print "Definition:",answer.definition
# print