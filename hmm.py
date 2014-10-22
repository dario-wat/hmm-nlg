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

class ChunkWrapper:

	# test and train sentences for chunk parser
	test_sents = conll2000.chunked_sents('test.txt', chunk_types=['NP'])
	train_sents = conll2000.chunked_sents('train.txt', chunk_types=['NP'])

	def __init__(self, train=train_sents):
		"""
		Creating chunk parser, and training it with conll2000 corpus.
		
		:train type: list(list(tuple))
		"""
		self._chunkParser = NEChunkParser(train)

	def parse(self, sent):
		"""
		Chunks given sentence, returns chunked tagged sentence.

		:sent type: list(tuple)
		:rtype: list(tuple)
		"""
		return ChunkWrapper._extractFromTree(self._chunkParser.parse(sent))

	@staticmethod
	def _convertChunk(chunk):
		"""
		Converts chunk into tuple consisting of string and tag.

		:chunk type: nltk.tree.Tree or tuple
		:rtype: tuple
		"""

		try:						# in case of Tree
			tag = chunk.label()
			phrase = ' '.join(map(itemgetter(0), chunk))
			return (phrase, tag)
		except AttributeError:		# in case of tuple
			return chunk

	@staticmethod
	def _extractFromTree(tree):
		"""
		Extracts words/phrases from tree structure defined by nltk. Returns
		all nodes on level 1.

		:tree type: nltk.tree.Tree
		:rtype: list(str)
		"""
		return map(ChunkWrapper._convertChunk, tree)

	def evaluate(self, test=test_sents):
		"""
		Evaluates chunk parser on the test set.

		:test type: list(list(tuple))
		:rtype: str
		"""
		return self._chunkParser.evaluate(test)


class HmmWrapper:
		pass


# logging settings, prints everything to stderr
logging.basicConfig(format='%(levelname)s\n:%(message)s', level=logging.DEBUG)



if __name__ == '__main__':
		
	logging.info('Training chunk parser...')
	chunker = ChunkWrapper()

	# supervised training
	corpus = map(lambda s: chunker.parse(s), brown.tagged_sents(categories='news'))

	states = unique_list(tag for sent in corpus for (word,tag) in sent)
	symbols = unique_list(word for sent in corpus for (word,tag) in sent)

	# unsupervised training

	# symbols = list(set([ss[0] for sss in seq for ss in sss]))
	# states = range(20)
	# m = trainer.train_unsupervisedseq, max_iterations=30)
	#states = symbols

	trainer = hmm.HiddenMarkovModelTrainer(states=states,symbols=symbols)
	hmmTrained = trainer.train_supervised(corpus)
	
	print ' '.join(map(lambda (x, _): x, hmmTrained.random_sample(random.Random(),50)))
