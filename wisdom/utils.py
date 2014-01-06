# This Python file uses the following encoding: utf-8
import nltk                   
from nltk.corpus import stopwords


def is_punctuation(c):
        return (len(c) == 1 and (c in "-.'?!,\":;()|-/")) or c == '""' or  len(c) == 1 or c == '--' or c == ').' or c == '.""' or c == ''
    
def tokenize(text, only_alpha = False, only_alphanum = True,  clean_stop_words = False, clean_punctuation = True):  

    tokens = nltk.wordpunct_tokenize(text)
    tokens = [t for t in tokens if (not clean_punctuation or not is_punctuation(t)) 
        and (not only_alpha or t.isalpha())
        and (not only_alphanum or t.isalnum())
        and (not clean_stop_words or t not in stopwords.words('english'))]          
    return tokens