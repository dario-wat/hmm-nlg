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
	parser = OptionParser(usage='usage: %prog [options]')
	parser.add_option('-f', '--filename', dest='filename', type='string',
		help='Corpus file')
	parser.add_option('-l', '--log', dest='logFlag',
		help='Print log to console', default=False, action='store_true')
	parser.add_option('-t', '--type', dest='type', type='choice',
		help="""Type of generation:
				super=supervised,
				unsuper=unsupervised,
				chunk=chunked supervised,
				all=precomputes all""",
		choices=['super', 'unsuper', 'chunk', 'all'], default='super')
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


def hmmFactory(trainType, string):
	"""
	Creates hmm by it's type and the given corpus.

	:trainType type: str
	:string type: str
	:rtype: HmmWrapper
	"""

	if trainType == 'super':			# supervised
		
		logging.info('Supervised')
		
		logging.info('Filtering corpus...')		
		corpus = tag(string)
		states = unique_list(tag for sent in corpus for (_,tag) in sent)
		symbols = unique_list(word for sent in corpus for (word, _) in sent)
		
		logging.info('Training hmm...')
		trainer = HmmWrapper(states, symbols)
		trainer.trainSupervised(corpus)

		return trainer

	elif trainType == 'unsuper':		# unsupervised
		
		logging.info('Unsupervised')

		logging.info('Filtering corpus')
		corpus = tagEmpty(string)
		states = range(5)
		symbols = unique_list(word for sent in corpus for (word, _) in sent)
		
		logging.info('Training hmm...')
		trainer = HmmWrapper(states, symbols)
		trainer.trainUnsupervised(corpus)
		
		return trainer

	else:							# chunked supervised
		
		logging.info('Chunked supervised')

		logging.info('Training chunk parser...')
		chunker = ChunkWrapper()
		
		logging.info('Chunking corpus...')
		corpus = tagChunk(string, chunker)
		states = unique_list(tag for sent in corpus for (_, tag) in sent)
		symbols = unique_list(word for sent in corpus for (word, _) in sent)
		
		logging.info('Training hmm...')
		trainer = HmmWrapper(states, symbols)
		trainer.trainSupervised(corpus)

		return trainer


def loopOnce(gen):
	"""
	Used for generating text after hmm has been trained. Exits when number
	less than 0 has been given.

	:gen type: HmmWrapper
	"""
		
	try:
		print 'Text length:'
		n = input()
		if n < 0:
			return
		
		print 'Generating...'
		print '=================================='
		print gen.generate(n)
		print '=================================='
	except ValueError:
		print 'Could not parse it'


def main():
	opt, _ = parseArguments()

	if opt.filename is None:
		raise StandardError('Corpus file required')

	if opt.logFlag:
		# logging settings, prints everything to stderr
		logging.basicConfig(format='[%(levelname)s] %(message)s', level=logging.DEBUG)

	# read file
	logging.info('Reading file: ' + opt.filename)
	f = open(opt.filename)
	string = f.read()
	f.close()

	# create hmm generator
	if opt.type == 'all':		# create all
		supGen = hmmFactory('super', string)
		unsupGen = hmmFactory('unsuper', string)
		chunkGen = hmmFactory('chunk', string)
		
		while 1:
			print 'Generator Type (s=super, u=unsuper, c=chunk)'
			t = raw_input()
			
			# generator choice
			gen = None
			if 		t == 's':	gen = supGen
			elif	t == 'u':	gen = unsupGen
			elif	t == 'c':	gen = chunkGen
			else:
				print 'Incorrect type'
				continue
			
			loopOnce(gen)

	else:						# create specific
		gen = hmmFactory(opt.type, string)
		while 1:
			loopOnce(gen)


if __name__ == '__main__':
	main()
	