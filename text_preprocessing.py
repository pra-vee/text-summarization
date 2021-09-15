#!/usr/bin/env python
# coding: utf-

import re
import string

from collections import Counter

import nltk

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


stops = stopwords.words('english')
wordnet_lemmatizer = WordNetLemmatizer()


translator = str.maketrans('', '', string.punctuation)

def text_preprocessing(text):
    text = text.lower()
    #text.translate(translator)
    text = re.sub("[,';:@#?!&$\[\]_]+", "", text)
    return text

def word_tokenizer(text):
    text = re.sub('\.', '', text)
    text = text_preprocessing(text)
    return [word for word in word_tokenize(text) if len(word) > 1]
    
def sent_tokenizer(text):
    text = text_preprocessing(text)
    return sent_tokenize(text)

def word_lemmatizer(words):
    lemmatized_words = []
    for word in words:
        lemmatized_words.append(wordnet_lemmatizer.lemmatize(word, pos='v'))
    return lemmatized_words