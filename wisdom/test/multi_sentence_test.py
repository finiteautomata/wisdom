#! coding:utf-8
from unittest import TestCase
from nltk.corpus import wordnet as wn
from wisdom import multi_sentence

class MultiSentenceTest(TestCase):
    def test_for_one_sentence(self):
        sent = 'I went to the bank to deposit my money'

        self.assertEqual(multi_sentence([sent], 'bank'), wn.synset('depository_financial_institution.n.01')) 

    def test_for_two_equal_sentences(self):
        sentences = ['I went to the bank to deposit my money',
            'I went to the bank to deposit my money']

        self.assertEqual(multi_sentence(sentences, 'bank'), wn.synset('depository_financial_institution.n.01')) 

    def test_for_two_senses_and_one_prevailing(self):
        sentences = [
            'I went to the bank to deposit my money',
            'The river bank was full of dead fishes',
            'The river bank was full of dead fishes'
            ]

        self.assertEqual(multi_sentence(sentences, 'bank'), wn.synset("bank.n.01"))
