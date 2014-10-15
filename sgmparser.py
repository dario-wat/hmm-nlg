from bs4 import BeautifulSoup
from sys import argv

def tagToString(tag):
	"""Takes the string of an SGML tag. String in this case is the content."""
	return tag.string

def filterNones(li):
	"""Yeah."""
	return filter(lambda t: t is not None, li)

class SGMLParser:
	"""For parsing some of the SGML things."""

	def __init__(self, string, lazy=True):
		"""
		Constructor. Takes a string to parse and another parameter for type
		of loading. Lazy - loads when asked for, eager - loads now.
		"""

		self._string = string
		self._soup = None
		if not lazy: self._load()
		self._titles = None
		self._topics = None
		self._texts = None

	def _load(self):
		"""Loads."""
		if self._soup is None:
			self._soup = BeautifulSoup(self._string)

	def titles(self):
		"""Returns all the news titles."""
		self._load()
		if self._titles is None:
			self._titles = filterNones(map(tagToString, self._soup('title')))
		return self._titles		

	def topics(self):
		"""Returns all topics."""
		self._load()
		if self._topics is None:
			self._topics = filterNones(map(tagToString, self._soup('topics')))
		return self._topics

	def texts(self):
		"""
		Returns all texts. Also because the reuters files are messed up,
		it filters out some tags inside text.
		"""
		
		self._load()
		if self._texts is None:
			self._texts = self._soup('text')
			for t in self._texts:
				if t.title is not None:		t.title.decompose()
				if t.dateline is not None:	t.dateline.decompose()
			self._texts = map(lambda t: t.get_text(), self._texts)
		return self._texts
