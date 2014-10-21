from nltk.chunk.named_entity import NEChunkParser
from nltk.corpus import brown, conll2000
from nltk import sent_tokenize, word_tokenize, pos_tag

from utils import *

def extractFromTree(tree):
	"""
	Extracts words/phrases from tree structure defined by nltk. Returns
	all nodes on level 1.

	:tree type: nltk.tree.Tree
	:rtype: list(str)
	"""

	


import logging

# logging settings, prints everything to stderr
logging.basicConfig(format='%(levelname)s\n:%(message)s', level=logging.DEBUG)

# test and train sentences for chunk parser
test_sents = conll2000.chunked_sents('test.txt', chunk_types=['NP'])
train_sents = conll2000.chunked_sents('train.txt', chunk_types=['NP'])

# creating chunk parser, and training it with conll2000 corpus
chunkParser = NEChunkParser(train_sents)
logging.info(chunkParser.evaluate(test_sents))


ss = brown.tagged_sents()

for i in xrange(20):
	print ss[i]
	print chunkParser.parse(ss[i])

