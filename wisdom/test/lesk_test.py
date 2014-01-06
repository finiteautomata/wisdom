#! coding:utf-8

from unittest import TestCase
from nltk.corpus import wordnet as wn
from wisdom import lesk

class LeskTest(TestCase):
    def test_for_financial_bank_sense_it_returns_that_one(self):
        sent = 'I went to the bank to deposit my money'

        self.assertEqual(lesk(sent, 'bank'), wn.synset('depository_financial_institution.n.01')) 

    def test_for_river_bank_sense(self):
        sent = 'The river bank was full of dead fishes'

        self.assertEqual(lesk(sent, 'bank'), wn.synset("bank.n.01"))


    def test_for_industrial_plant_sense(self):
        sent = 'The workers at the industrial plant were overworked'

        self.assertEqual(lesk(sent, 'plant'), wn.synset("plant.n.01"))
