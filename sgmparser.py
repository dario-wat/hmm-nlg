from bs4 import BeautifulSoup
from sys import argv

def tagToString(tag):
	return tag.string

def filterNones(li):
	return filter(lambda t: t is not None, li)

class SGMLParser:

	def __init__(self, string, lazy=True):
		self._string = string
		self._soup = None
		if not lazy: self._load()
		self._titles = None
		self._topics = None
		self._texts = None

	def _load(self):
		if self._soup is None:
			self._soup = BeautifulSoup(self._string)

	def titles(self):
		self._load()
		if self._titles is None:
			self._titles = filterNones(map(tagToString, self._soup('title')))
		return self._titles		

	def topics(self):
		self._load()
		if self._topics is None:
			self._topics = filterNones(map(tagToString, self._soup('topics')))
		return self._topics

	def texts(self):
		self._load()
		if self._texts is None:
			self._texts = self._soup('text')
			for t in self._texts:
				if t.title is not None:		t.title.decompose()
				if t.dateline is not None:	t.dateline.decompose()
			self._texts = map(lambda t: t.get_text(), self._texts)
		return self._texts
