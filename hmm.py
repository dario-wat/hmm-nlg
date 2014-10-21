
import nltk.tag.hmm as hmm
import nltk
import sys
from nltk.util import unique_list

import random
from sys import argv


s = """I am trying to use stupid hmm to generate a random sentence. This random sentence
                is supposed to be very good, good"""

try:
    f= open(sys.argv[1])
except IndexError:
    f = open('rawcorpus/andersen.txt')

s= f.read()
f.close()

s = s[0:3000]

# supervised training

corpus = nltk.corpus.brown.tagged_sents(categories='news')[:3000]

states = unique_list(tag for sent in corpus for (word,tag) in sent)
symbols = unique_list(word for sent in corpus for (word,tag) in sent)

sentences = nltk.sent_tokenize(s)

tag_set = unique_list(tag for sent in corpus for (word,tag) in sent)
seq = [map(lambda x:(x,''), ss.split()) for ss in sentences]
#seq = [word for sent in sentences for word in nltk.word_tokenize(sent)]

# unsupervised training

# symbols = list(set([ss[0] for sss in seq for ss in sss]))
# states = range(20)

#states = symbols
trainer = nltk.tag.hmm.HiddenMarkovModelTrainer(states=states,symbols=symbols)

hmm = trainer.train_supervised(corpus)
# m = trainer.train_unsupervisedseq, max_iterations=30)

# print ' '.join(map(lambda (x, _): x, hmm.random_sample(random.Random(),50)))
print ' '.join(map(lambda (x, _): x, hmm.random_sample(random.Random(),30)))


class HmmWrapper:
