from sgmparser import SGMLParser

lo = 0
hi = 22
filePattern = ('reut2-', '.sgm')
fileIndices = xrange(lo, hi)
folder = '../reuters21578/'

def filename(index):
	return folder + filePattern[0] + str(index).zfill(3) + filePattern[1]

class Loader:
	"""
	Used for loading sgm files into memory. Class is able to use lazy
	or eager technique of loading. Each SGMLParser can be accessed in
	three ways:

	loader = Loader()

	1. method 'parser'
		loader.parser(index)
	2. get item
		loader[index]
	3. instance call
		loader(index)
	"""

	def __init__(self, lazy=True):
		self._parsers = []
		self._lazy = lazy
		laziness = "Lazy" if self._lazy else "Eager"
		for i in fileIndices:
			with open(filename(i)) as f:
				print 'Loading...', '(' + laziness + ')', filename(i)
				self._parsers.append(SGMLParser(f.read(), lazy))

	def __getitem__(self, key):
		return self.parser(key)

	def __call__(self, key):
		return self.parser(key)

	def parser(self, index):
		if index < lo or index >= hi:
			raise StandardError("You Fool!")
		return self._parsers[index]
