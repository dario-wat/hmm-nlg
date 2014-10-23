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

def tagOnly(string):
	"""Tokenizes string and tags it. Returns a list of tagged sentences with just tags and not words."""
	return map(lambda s: [tag for (word,tag) in pos_tag(word_tokenize(s))], sent_tokenize(string))

def tagEmpty(string):
	"""Tokenizes string and tags it with empty strings. Returns a list of
	tagged sentences."""
	return [map(lambda w: (w, ''), sent) for sent in tokenize(string)]

def tokenize(string):
	"""Tokenizes a string into a list of list of words (list of sentences)."""
	return map(word_tokenize, sent_tokenize(string))

def tagChunk(string, chunker):
	"""Tokenizes a string and chunks the sentences."""
	return map(lambda s: chunker.parse(s), tag(string))