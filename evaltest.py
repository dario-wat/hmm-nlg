from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import brown
import ngram
import sys
from evaluate.evaluate import Evaluate
from hmm import *
def ngramEval(sents, evalf, nrGenerations):
	print "Starting Ngram generation and scoring"
	trigram = ngram.Ngram(3, brown.words())
	f = open("DataNgram.txt",'a')
	for i in range(0,nrGenerations):
		print i
		sample =  trigram.generate(30, afterModify=ngram.endSentence)
		evalf.setTarget(sample)
		scoreB = evalf.Bleu(sample)
		scorePos = evalf.POSChecker(sents)
		scoreLC = evalf.lctest()
		s = "%.3f \t\t%.3f \t\t%.3f \t\t" % (scoreB, scoreLC, scorePos)
		s += sample + "\n"
		f.write(s)
	f.close()
	print "Ngram generation and evaluation complete"

def humanEval(sents, evalf, infile):
	print "Starting human scoring"
	i = open(infile)
	f = open("DataHuman.txt",'a')
	turn = 0
	for line in i:
		print turn
		evalf.setTarget(line)
		scoreB = evalf.Bleu(line)
		scorePos = evalf.POSChecker(sents)
		scoreLC = evalf.lctest()
		s = "%.3f \t\t%.3f \t\t%.3f \t\t" % (scoreB, scoreLC, scorePos)
		s += line
		f.write(s)
		turn +=1
	f.close()
	i.close()
	print "Human evaluation complete"

def hmmEval(sents, evalf, trainType, corpus, nrGenerations):
	print "HMM evaluation started for " + trainType
	f = open("HMM"+trainType+".txt","a")
	s = open(corpus)
	string = s.read()
	trainer = hmmFactory(trainType,string)
	for i in range(0,nrGenerations):
		print i
		sample = trainer.generate(30)
		evalf.setTarget(sample)
		scoreB = evalf.Bleu(sample)
		scorePos = evalf.POSChecker(sents)
		scoreLC = evalf.lctest()
		s = "%.3f \t\t%.3f \t\t%.3f \t\t" % (scoreB, scoreLC, scorePos)
		s += sample + "\n"
		f.write(s)
	f.close()
	s.close()
	print "HMM evaluation completed for " +trainType

def evalAllHmm(sents, evalf, corpus, nrGenerations):
	hmmEval(sents, evalf, "super", corpus, nrGenerations)
	hmmEval(sents, evalf, "unsuper", corpus, nrGenerations)
	hmmEval(sents, evalf, "chunk", corpus, nrGenerations)

def main():
	corpussub = brown.sents()[:3000]
	#runCalc(corpussub)
	evalf = Evaluate()
	sents = map(lambda s: ' '.join(s), corpussub)
	finsents = reduce(lambda a,b: a + ' '+ b, sents)
	evalf.initBleu(sents)
	#ngramEval(finsents,evalf,10)
	#humanEval(finsents, evalf, "rawcorpus/humansentence.txt")
	evalAllHmm(finsents, evalf,"rawcorpus/andersen.txt",5)

if __name__ == "__main__":
	main()