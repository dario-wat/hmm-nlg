"""
import nltk
from loader import Loader

l = Loader()
tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+|[^\w\s]+')

content_text = ' '.join(l(0).texts())
tokenized_content = tokenizer.tokenize(content_text)
content_model = nltk.NgramModel(3, tokenized_content)

starting_words = content_model.generate(100)[-2:]
content = content_model.generate(100, starting_words)
print ' '.join(content)
"""

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import brown
import ngram
import sys
from evaluate.evaluate import Evaluate

string = ''
if len(sys.argv) > 1:
	for i in xrange(1, len(sys.argv)):
		try:
			f = open(sys.argv[i])
		except:
			continue
		string += f.read()
		f.close()
else:
    f = open('rawcorpus/andersen.txt')
    string = f.read()
    f.close()

#string = brown
#print len(string)
#print len(string.split())
print len(brown.words())

trigram = ngram.Ngram(3, brown.words())
sample =  trigram.generate(30, afterModify=ngram.endSentence)
print sample
corpussub = brown.sents()[:3000]
sents = map(lambda s: ' '.join(s), corpussub)
finsents = reduce(lambda a,b: a + ' '+ b, sents)
# print finsents
evalf = Evaluate()
evalf.setTarget(sample)
print evalf.POSChecker(finsents)
print evalf.lctest()
