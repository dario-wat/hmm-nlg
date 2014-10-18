
import nltk.tag.hmm as hmm
import nltk

import random
from sys import argv


s = """I am trying to use stupid hmm to generate a random sentence. This random sentence
                is supposed to be very good, good"""
with open(argv[1]) as f:
        s = f.read()

print len(s)
s = s[0:1000]
#print len(s)
sentences = nltk.sent_tokenize(s)
seq = [map(lambda x:(x,''), ss.split()) for ss in sentences]
#seq = [word for sent in sentences for word in nltk.word_tokenize(sent)]
symbols = list(set([ss[0] for sss in seq for ss in sss]))
print len(symbols)
print len([word for sent in sentences for word in nltk.word_tokenize(sent)])
states = symbols
trainer = nltk.tag.hmm.HiddenMarkovModelTrainer(states=states,symbols=symbols)
m = trainer.train_unsupervised(seq, max_iterations=30)
print ' '.join(map(lambda (x, _): x, m.random_sample(random.Random(),30)))