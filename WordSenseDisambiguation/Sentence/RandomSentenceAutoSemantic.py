import random

from AnnotatedSentence.AnnotatedSentence import AnnotatedSentence
from MorphologicalAnalysis.FsmMorphologicalAnalyzer import FsmMorphologicalAnalyzer
from WordNet.WordNet import WordNet

from WordSenseDisambiguation.Sentence.SentenceAutoSemantic import SentenceAutoSemantic


class RandomSentenceAutoSemantic(SentenceAutoSemantic):

    __turkish_wordnet: WordNet
    __fsm: FsmMorphologicalAnalyzer

    def __init__(self, turkishWordNet: WordNet, fsm: FsmMorphologicalAnalyzer):
        self.__turkish_wordnet = turkishWordNet
        self.__fsm = fsm

    def autoLabelSingleSemantics(self, sentence: AnnotatedSentence) -> bool:
        random.seed(1)
        for i in range(sentence.wordCount()):
            syn_sets = self.getCandidateSynSets(self.__turkish_wordnet, self.__fsm, sentence, i)
            if len(syn_sets) > 0:
                sentence.getWord(i).setSemantic(syn_sets[random.randrange(len(syn_sets))].getId())
        return True
