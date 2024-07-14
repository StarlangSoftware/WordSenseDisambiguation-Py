import random

from AnnotatedSentence.AnnotatedSentence import AnnotatedSentence
from MorphologicalAnalysis.FsmMorphologicalAnalyzer import FsmMorphologicalAnalyzer
from WordNet.WordNet import WordNet

from WordSenseDisambiguation.Sentence.SentenceAutoSemantic import SentenceAutoSemantic


class RandomSentenceAutoSemantic(SentenceAutoSemantic):

    __turkish_wordnet: WordNet
    __fsm: FsmMorphologicalAnalyzer

    def __init__(self, turkishWordNet: WordNet, fsm: FsmMorphologicalAnalyzer):
        """
        Constructor for the {@link RandomSentenceAutoSemantic} class. Gets the Turkish wordnet and Turkish fst based
        morphological analyzer from the user and sets the corresponding attributes.
        :param turkishWordNet: Turkish wordnet
        :param fsm: Turkish morphological analyzer
        """
        self.__turkish_wordnet = turkishWordNet
        self.__fsm = fsm

    def autoLabelSingleSemantics(self, sentence: AnnotatedSentence) -> bool:
        """
        The method annotates the word senses of the words in the sentence randomly. The algorithm processes target
        words one by one. First, the algorithm constructs an array of all possible senses for the target word to
        annotate. Then it chooses a sense randomly.
        :param sentence: Sentence to be annotated.
        :return: True.
        """
        random.seed(1)
        for i in range(sentence.wordCount()):
            syn_sets = self.getCandidateSynSets(self.__turkish_wordnet, self.__fsm, sentence, i)
            if len(syn_sets) > 0:
                sentence.getWord(i).setSemantic(syn_sets[random.randrange(len(syn_sets))].getId())
        return True
