from nltk.corpus import brown, conll2000
from nltk.util import unique_list
from nltk.chunk.named_entity import NEChunkParser
from nltk import sent_tokenize, word_tokenize, pos_tag

import nltk.tag.hmm as hmm
import nltk

from utils import *

from sys import argv
from operator import itemgetter

import random
import logging

# logging settings, prints everything to stderr
logging.basicConfig(format='%(levelname)s\n:%(message)s', level=logging.DEBUG)

if __name__ == '__main__':
	
	# test and train sentences for chunk parser
	test_sents = conll2000.chunked_sents('test.txt', chunk_types=['NP'])
	train_sents = conll2000.chunked_sents('train.txt', chunk_types=['NP'])

	# creating chunk parser, and training it with conll2000 corpus
	chunkParser = NEChunkParser(train_sents)
	logging.info(chunkParser.evaluate(test_sents))

	
	s = """I am trying to use stupid hmm to generate a random sentence. This random sentence
	                is supposed to be very good, good"""
	ss = tag(s)

	print chunkParser.parse(ss[0])
	#try:
	#    f= open(sys.argv[1])
	#except IndexError:
	#    f = open('rawcorpus/andersen.txt')

	#s= f.read()
	#f.close()

	#s = s[0:3000]

	# supervised training

	#corpus = nltk.corpus.brown.tagged_sents(categories='news')#[:3000]
	#corpus = conll2000.tagged_sents()
	#print corpus

	#states = unique_list(tag for sent in corpus for (word,tag) in sent)
	#symbols = unique_list(word for sent in corpus for (word,tag) in sent)

	#sentences = nltk.sent_tokenize(s)

	#tag_set = unique_list(tag for (word,tag) in corpus)
	#seq = [map(lambda x:(x,''), ss.split()) for ss in sentences]
	#seq = [word for sent in sentences for word in nltk.word_tokenize(sent)]

	# unsupervised training

	# symbols = list(set([ss[0] for sss in seq for ss in sss]))
	# states = range(20)

	#states = symbols
	#trainer = nltk.tag.hmm.HiddenMarkovModelTrainer(states=states,symbols=symbols)
	#print map(itemgetter(0), corpus)
	#hmm = trainer.train_supervised(corpus)
	# m = trainer.train_unsupervisedseq, max_iterations=30)

	#print ' '.join(map(lambda (x, _): x, hmm.random_sample(random.Random(),50)))


	class HmmWrapper:
		pass