from nltk.corpus import brown, conll2000
from nltk.util import unique_list
from nltk.chunk.named_entity import NEChunkParser
from nltk import sent_tokenize, word_tokenize, pos_tag

import nltk.tag.hmm as hmm
import nltk

from utils import *

from sys import argv
from operator import itemgetter
from optparse import OptionParser

import random
import logging

def parseArguments():
	parser = OptionParser()
	parser.add_option('-f', '--filename', dest='filename', type='string',
		help='Corpus file')
	parser.add_option('-l', '--log', dest='logFlag',
		help='Print log to console', default=False, action='store_true')
	parser.add_option('-t', '--type', dest='type', type='choice',
		help="""Type of generation:
				super=supervised,
				unsuper=unsupervised,
				chunk=chunked supervised""",
		choices=['super', 'unsuper', 'chunk'], default='super')
	return parser.parse_args()


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
	
	def __init__(self, states, symbols):
		"""
		Constructs trainer/hmm using states and symbols.

		:states type: list
		:symbols type: list(tuple)
		"""

		self._hmm = None
		self._trainer = hmm.HiddenMarkovModelTrainer(states=states, symbols=symbols)

	def trainSupervised(self, labeledCorpus):
		"""
		Trains hmm with labeled corpus.

		:labeledCorpus type: list(list(tuple))
		:rtype: nltk.tag.hmm.HiddenMarkovModelTagger
		"""
		self._hmm = self._trainer.train_supervised(labeledCorpus)

	def trainUnsupervised(self, unlabeledCorpus, maxIter=10):
		"""
		Trains hmm with unlabeled corpus. Unlabeled corpus is exactly like
		labeled, but the tags are empty strings.

		:unlabeledCorpus type: list(list(tuple))
		:rtype: nltk.tag.hmm.HiddenMarkovMode
		"""
		self._hmm = self._trainer.train_unsupervised(unlabeledCorpus, max_iterations=maxIter)

	def generate(self, length=20):
		"""
		Generates random sequence of a at least 'length' words.

		:length type: int
		:rtype: str
		"""

		if self._hmm is None:
			raise StandardError('Hmm not trained')
		return ' '.join(map(lambda (x, _): x, self._hmm.random_sample(random.Random(), length)))


def main():
	opt, _ = parseArguments()

	if opt.filename is None:
		raise StandardError('Corpus file required')

	if opt.logFlag:
		# logging settings, prints everything to stderr
		logging.basicConfig(format='%(levelname)s\n:%(message)s', level=logging.DEBUG)

	# read file
	logging.info('Reading file: ' + opt.filename)
	f = open(opt.filename)
	string = f.read()
	f.close()

	if opt.type == 'super':			# supervised
		logging.info('Supervised')
		
		logging.info('Filtering corpus...')		
		corpus = tag(string)
		states = unique_list(tag for sent in corpus for (_,tag) in sent)
		symbols = unique_list(word for sent in corpus for (word, _) in sent)
		
		logging.info('Training hmm...')
		trainer = HmmWrapper(states, symbols)
		trainer.trainSupervised(corpus)

		print trainer.generate()

	elif opt.type == 'unsuper':		# unsupervised
		logging.info('Unsupervised')

		logging.info('Filtering corpus')
		corpus = tagEmpty(string)
		states = range(5)
		symbols = unique_list(word for sent in corpus for (word, _) in sent)
		
		logging.info('Training hmm...')
		trainer = HmmWrapper(states, symbols)
		trainer.trainUnsupervised(corpus)
		
		print trainer.generate()
		
	else:							# chunked supervised
		logging.info('Chunked supervised')

		logging.info('Training chunk parser...')
		chunker = ChunkWrapper()
		
		logging.info('Chunking corpus...')
		corpus = map(lambda s: chunker.parse(s), tag(string))	
		states = unique_list(tag for sent in corpus for (word,tag) in sent)
		symbols = unique_list(word for sent in corpus for (word,tag) in sent)
		
		logging.info('Training hmm...')
		trainer = HmmWrapper(states, symbols)
		trainer.trainSupervised(corpus)

		print trainer.generate()



if __name__ == '__main__':
	main()
	