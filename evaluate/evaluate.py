__author__ = 'akashdhaka'

import language_check
import math
from nltk.tokenize import sent_tokenize
from nltk import pos_tag
import difflib
import utils
import nltk

class Evaluate:

    def __init__(self):
        self._lcevaluator = language_check.LanguageTool('en-US')


    def setTarget(self, target):
        self.target = target


    def lctest(self):
        matches = self._lcevaluator.check(self.target)
        words = utils.tokenize(self.target)
        self.precisionLC = 2/ (1+ math.exp(len(matches)/len(words)))
        return self.precisionLC


    def POSChecker(self, corpus):
        sentences = sent_tokenize(corpus)
        tagList = utils.tagOnly(corpus)
        tagListpat = map(lambda s: ' '.join(s), tagList)
        # print tagListpat
        targetPOS = [tag for (word,tag) in nltk.pos_tag(nltk.word_tokenize(self.target))]
        tpospat = ' '.join(targetPOS)
        # print str(tpospat)
        respat = map( lambda s:  difflib.SequenceMatcher(None, tpospat, s).ratio(), tagListpat )
        self.precisionPOS = max(respat)
        return self.precisionPOS


        # taglist = map(lambda x: tag for (word, tag) in nltk.pos_tag(x))
        # taglist = [tag for sent in sentences for (word,tag) in nltk.pos_tag(sent)]




if __name__ == '__main__':
    text = 'Time passed merrily in the large town which was his capital; strangers arrived every day at the court. One day, two rogues, calling themselves weavers, made their appearance.'
    test = 'Time passed merrily in the large town.'
    eval = Evaluate('pos')
    eval.setTarget(test)
    eval.POSChecker(text)
