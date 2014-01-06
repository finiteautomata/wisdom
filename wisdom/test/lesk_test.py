#! coding:utf-8
from unittest import TestCase
from nltk.corpus import wordnet as wn
from wisdom import lesk

class LeskTest(TestCase):
    def test_for_financial_bank_sense_it_returns_that_one(self):
        sent = 'I went to the bank to deposit my money'

        self.assertEqual(lesk(sent, 'bank'), wn.synset('depository_financial_institution.n.01')) 

