#!/usr/bin/env python
# coding: utf-8

import requests
from bs4 import BeautifulSoup

import text_preprocessing as txt

import streamlit as st

import pandas as pd
import numpy as np

import re
import string
import math
import heapq

from collections import Counter

np.random.seed(1234)


############# Text Analysis and TF-IDF #############


def get_word_freq(corpus):
    word_freq_matrix = {}
    
    for sentence in corpus:
        word_frequency = {}

        words = txt.word_tokenizer(sentence)
        n_words = len(words)
        words = txt.word_lemmatizer(words)

        for word in words:
            if word not in txt.stops:
                if word in word_frequency.keys():
                    word_frequency[word] += 1
                else:
                    word_frequency[word] = 1
            
        word_freq_matrix[hash(sentence)]  = word_frequency
    
    return word_freq_matrix


def get_docs_per_word(word_freq_matrix):
    docs_per_word = {}
    
    for key, word_frequency in word_freq_matrix.items():
        for word, count in word_frequency.items():
            if word in docs_per_word:
                docs_per_word[word] += 1
            else:
                docs_per_word[word] = 1
    
    return docs_per_word


def get_tf_matrix(word_freq_matrix):
    tf_matrix = {}
    
    for key, word_frequency in word_freq_matrix.items():
        tf = {}
        
        n_words = len(word_frequency)
        for word, count in word_frequency.items():
            tf[word] = count/n_words
            
        tf_matrix[key] = tf
    
    return tf_matrix



def get_idf_matrix(word_freq_matrix, docs_per_word, n_docs):
    idf_matrix = {}
    
    for key, word_frequency in word_freq_matrix.items():
        idf = {}
        
        for word in word_frequency.keys():
            idf[word] = math.log10(n_docs/(float(docs_per_word[word]) + 1))
        
        idf_matrix[key] = idf
    
    return idf_matrix


def get_tf_idf_matrix(tf_matrix, idf_matrix):
    tf_idf_matrix = {}

    for (key1, word_freq1), (key2, word_freq2) in zip(tf_matrix.items(), idf_matrix.items()):

        tf_idf = {}

        for (word1, tf), (word2, idf) in zip(word_freq1.items(), word_freq2.items()):
            tf_idf[word1] = float(tf * idf)

        tf_idf_matrix[key1] = tf_idf
    
    return tf_idf_matrix


def get_sentence_score(tf_idf_matrix):
    sentence_score = {}
    
    for key, val_dict in tf_idf_matrix.items():
        score = 0
        for word, tf_idf in val_dict.items():
            score += tf_idf
            
        sentence_score[key] = score
    
    #print(sentence_score)
    return sentence_score


def get_summary(n_sentences_to_retain, corpus):
    
    n_docs = len(corpus)
    
    word_freq_matrix = get_word_freq(corpus)
    docs_per_word = get_docs_per_word(word_freq_matrix)

    tf_matrix = get_tf_matrix(word_freq_matrix)
    idf_matrix = get_idf_matrix(word_freq_matrix, docs_per_word, n_docs)
    tf_idf_matrix = get_tf_idf_matrix(tf_matrix, idf_matrix)

    sentence_scores = get_sentence_score(tf_idf_matrix)

    top_n = heapq.nlargest(n_sentences_to_retain, sentence_scores, key=sentence_scores.get)
    #print(top_n)
    
    summary = []

    for sentence in corpus:
        if hash(sentence) in top_n:
            #print(sentence_scores[hash(sentence)])
            summary.append(sentence)
            #print(sentence + '\n_______________')
        else:
            pass
    
    return " ".join(summary)


############# Get Inputs #############


def get_url():
    url = st.text_input('Enter URL of text to summarize:')
    return url


def get_percentage_to_retain():
    v = st.slider("Enter Percentage to Retain (0-100):", min_value=0, max_value=100, value=15, step=5)
    return v
        

def get_corpus(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    content = " ".join(p.text for p in soup.find_all('p'))
    content = re.sub('\n+', ' ', content)
    corpus = txt.sent_tokenizer(content)
    return corpus


############# Streamlit App #############


def main():
    st.title("Text Summarization")

    st.header("Methodology")
    body="""
- Get inputs: 
    - URL
    - precentage to retain
- Retrieve content from URL
- Calculate number of sentences(_n_) based on percentage to retain
- Calculate the tf-idf value for each word(_lemma_) in every sentence(_document_)
- Aggregate tf-idf value for each sentence to get relative importance across the text(_corpus_)
- Sort sentences by importance and take top _n_
- Retrieve original sentence and concatenate to form summary
    """
    st.markdown(body)

    st.header("User Inputs")

    url = get_url()
    percentage_to_retain = get_percentage_to_retain()

    if url != "":
        try:
            corpus = get_corpus(url)

            n_sentences_to_retain = int((percentage_to_retain * len(corpus))/100)
            summary = get_summary(n_sentences_to_retain, corpus)

            st.header("Summary of Text")
            st.write(summary)

        except Exception as e:
            st.error(e)


if __name__ == "__main__":
    main()