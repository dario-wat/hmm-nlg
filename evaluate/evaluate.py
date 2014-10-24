__author__ = 'akashdhaka'

import language_check
import math
from nltk.tokenize import sent_tokenize
from nltk import pos_tag
from nltk import word_tokenize
from nltk.align.bleu import BLEU
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

    def initBleu(self, corpus):
        self.ref_tokens = corpus

    def Bleu(self, testText):
        w = [0.25, 0.25, 0.25, 0.25]
        total = 0.0
        count = 0
        for tokens in self.ref_tokens:
            candi_tokens = word_tokenize(testText)
            total = max(total, BLEU.modified_precision(candi_tokens,[tokens.split()],2))
            count+=1
        return total
        # taglist = map(lambda x: tag for (word, tag) in nltk.pos_tag(x))
        # taglist = [tag for sent in sentences for (word,tag) in nltk.pos_tag(sent)]

if __name__ == '__main__':
    text = 'Time passed merrily in the large town which was his capital; strangers arrived every day at the court. One day, two rogues, calling themselves weavers, made their appearance.'
    test = 'Had the luxury to take some photos of this stunning beauty the other day. Im so proud to be her agent!'
    eval = Evaluate()
    #print eval.setTarget(test)
    #print eval.POSChecker(text)
    #print eval.lctest()
    print eval.Bleu("The Fulton County should receive the award .")