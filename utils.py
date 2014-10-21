from nltk import sent_tokenize, word_tokenize, pos_tag

def wordify(string):
	"""Takes a string end tokenizes it into a list of words."""
	words = []
	for sent in sent_tokenize(string):
		words += word_tokenize(sent)
	return words

def tag(string):
	"""Tokenizes string and tags it. Returns a list of tagged sentences."""
	return map(lambda s: pos_tag(word_tokenize(s)), sent_tokenize(string))