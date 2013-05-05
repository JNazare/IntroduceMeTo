from __future__ import division
import nltk, re, pprint

raw = open('raw_twitter_corpus.txt').read()
print type(raw)
tokens = nltk.word_tokenize(raw)
print type(tokens)
words = [w.lower() for w in tokens]
vocab = sorted(set(words))

print vocab