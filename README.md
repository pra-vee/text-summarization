# Text Summarization using tf-idf

## Goals of the Project

The goal of the project is to identify relatively important parts of any given text(which is automatically retrieved from an input URL) and summarize them in a coherent passage based on a user desired retention percentage.

## Approach

The text summarization is achieved using a combination of text lemmatization and the application of tf-idf to identify parts of the text that are relatively important.

## What is tf-idf?

Simply put, tf-idf helps understand how important a lemma(_think word_) is to a document(_think chapter_) in a collection or corpus(_think book_). It does this by weighing the frequently occuring words in a chapter more, while also offseting the value by the number of chapters in the book that contain the word.

## Methodology
Each corpus retrieved from the URL goes through the following steps:
- Get inputs 
	- URL
	- precentage to retain
- Retrieve content from URL
- Calculate number of sentences(_n_) based on percentage to retain
- Calculate tf-idf for each word(_lemma_) in every sentence(_document_)
- Aggregate tf-idf score for each sentence get relative importance across the text(_corpus_)
- Sort sentences by importance and take top _n_
- Retrieve original sentence and concatenate to form summary

