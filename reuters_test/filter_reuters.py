"""This module is hardcoded for filtering reuters files. Can be improved."""

from loader import Loader
import re

def intoFileNonFiltered():
	"""Reads all the files and writes all the texts into single file."""
	l = Loader()
	texts = [t for pars in l.iter() for t in pars.texts()]
	with open('not_filtered.txt', 'w') as f:
		f.write(' '.join(texts).encode('utf8'))

def filterFile():
	"""Filters file."""
	with open('not_filtered.txt') as nf, open('filtered.txt', 'w') as ff:
		string = nf.read()
		noExtraSpaces = string.replace('  ', ' ').replace('\t', '')		# remove extra space
		removedSomePhrases = noExtraSpaces.replace('Reuter', '')	\
			.replace('REUTER', '').replace('******Blah blah blah.', '')	# remove some useless words
		

		# re (regex) module can be used for additional modifications,
		# for example removing consecutive stars '*'
		#res = re.findall('[*]+', removedSomePhrases)
		#print '\n'.join(res)
		#res = re.sub('\W\W+', ' ', removedSomePhrases)
		
		ff.write(removedSomePhrases)	# write into new file

if __name__ == '__main__':
	filterFile()
	