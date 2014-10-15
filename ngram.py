from nltk.tokenize import RegexpTokenizer
from nltk.model.ngram import NgramModel
from nltk.probability import LidstoneProbDist

tokenizer = RegexpTokenizer(r'\w+|[^\w\s]+')

def tokenize(string):
	"""Tokenizes."""
	return tokenizer.tokenize(string)

def endSentence(string):
	"""Cuts the string at the last dot '.' . The return has a proper ending.""" 
	ind = string.rfind('.')
	return string if ind == -1 else string[0:ind+1]

def iden(string):
	"""Identity. Used for after modification of generated string."""
	return string

class Ngram:
	"""
	Usage:

	l = Loader()
	sentence = ' '.join(l(0).texts())
	ngram = Ngram(3, tokenize(sentence))
	s = ngram.generate(30)
	print endSentence(s)
	"""

	def __init__(self, n, corpus, est=None):
		"""
		Creates na n-gram with given n and corpus. Parameter est is yet to
		be implemented.
		"""
		
		self._n = n
		self._ngram = NgramModel(n, corpus)

	def _startingWords(self):
		"""
		Takes 2 words at the end of generated string. This is used for
		randomizing generator.
		"""
		
		return self._ngram.generate(100)[-2:]

	def _startSentence(self):
		"""
		Cuts out everything until the first dot '.' . That way, the generated
		text will be the beginning of a sentence.
		"""
		
		li = self._ngram.generate(100)
		return [li[(li.index('.') + 1) % 100]] if '.' in li else li[-2:]

	def generate(self, numWords, context=[], afterModify=iden):
		"""
		Generates a text of approximately numWords numer of words.
		Parameter context is used to start the sentence with something.
		Parameter afterModify is a function that is called on the generated
		string, it additionally modifies the string (for example, to end the
		sentence).
		"""
		
		result = self._ngram.generate(numWords, context) if len(context) > 0 \
			else self._ngram.generate(numWords, self._startSentence())
		return afterModify(' '.join(result))
