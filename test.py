"""
import nltk
from loader import Loader

l = Loader()
tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+|[^\w\s]+')

content_text = ' '.join(l(0).texts())
tokenized_content = tokenizer.tokenize(content_text)
content_model = nltk.NgramModel(3, tokenized_content)

starting_words = content_model.generate(100)[-2:]
content = content_model.generate(100, starting_words)
print ' '.join(content)
"""

import ngram
import sys

string = ''
with open(sys.argv[1]) as f:
	string = f.read()
print len(string)
print len(string.split())

trigram = ngram.Ngram(3, ngram.tokenize(string))
print trigram.generate(70, afterModify=ngram.endSentence)