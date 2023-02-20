from AnnotatedSentence.AnnotatedSentence import AnnotatedSentence
from AnnotatedSentence.AnnotatedWord import AnnotatedWord
from MorphologicalAnalysis.FsmMorphologicalAnalyzer import FsmMorphologicalAnalyzer
from WordNet.SynSet import SynSet
from WordNet.WordNet import WordNet

from WordSenseDisambiguation.Sentence.SentenceAutoSemantic import SentenceAutoSemantic


class MostFrequentSentenceAutoSemantic(SentenceAutoSemantic):
    __turkish_wordnet: WordNet
    __fsm: FsmMorphologicalAnalyzer

    def __init__(self, turkishWordNet: WordNet, fsm: FsmMorphologicalAnalyzer):
        self.__turkish_wordnet = turkishWordNet
        self.__fsm = fsm

    def mostFrequent(self, literals: list) -> SynSet:
        if len(literals) == 1:
            return self.__turkish_wordnet.getSynSetWithId(literals[0].getSynSetId())
        min_sense = 50
        best = None
        for literal in literals:
            if literal.getSense() < min_sense:
                min_sense = literal.getSense()
                best = self.__turkish_wordnet.getSynSetWithId(literal.getSynSetId())
        return best

    def autoLabelSingleSemantics(self, sentence: AnnotatedSentence) -> bool:
        done = False
        two_previous = None
        previous = None
        next = None
        two_next = None
        for i in range(sentence.wordCount()):
            current = sentence.getWord(i)
            if i > 1:
                two_previous = sentence.getWord(i - 2)
            if i > 0:
                previous = sentence.getWord(i - 1)
            if i != sentence.wordCount() - 1:
                next = sentence.getWord(i + 1)
            if i < sentence.wordCount() - 2:
                two_next = sentence.getWord(i + 2)
            if isinstance(current, AnnotatedWord) and current.getSemantic() is None and current.getParse() is not None:
                if two_previous is not None and isinstance(two_previous, AnnotatedWord) \
                        and two_previous.getParse() is not None and isinstance(previous, AnnotatedWord) \
                        and previous.getParse() is not None:
                    literals = self.__turkish_wordnet.constructIdiomLiterals(self.__fsm,
                                                                             two_previous.getParse(),
                                                                             two_previous.getMetamorphicParse(),
                                                                             previous.getParse(),
                                                                             previous.getMetamorphicParse(),
                                                                             current.getParse(),
                                                                             current.getMetamorphicParse())
                    if len(literals) > 0:
                        best_synset = self.mostFrequent(literals)
                        if best_synset is not None:
                            current.setSemantic(best_synset.getId())
                            done = True
                            continue
                if previous is not None and isinstance(previous, AnnotatedWord) \
                        and previous.getParse() is not None and next is not None and isinstance(next, AnnotatedWord) \
                        and next.getParse() is not None:
                    literals = self.__turkish_wordnet.constructIdiomLiterals(self.__fsm,
                                                                             previous.getParse(),
                                                                             previous.getMetamorphicParse(),
                                                                             current.getParse(),
                                                                             current.getMetamorphicParse(),
                                                                             next.getParse(),
                                                                             next.getMetamorphicParse())
                    if len(literals) > 0:
                        best_synset = self.mostFrequent(literals)
                        if best_synset is not None:
                            current.setSemantic(best_synset.getId())
                            done = True
                            continue
                if next is not None and isinstance(next, AnnotatedWord) \
                        and next.getParse() is not None and two_next is not None and isinstance(two_next, AnnotatedWord) \
                        and two_next.getParse() is not None:
                    literals = self.__turkish_wordnet.constructIdiomLiterals(self.__fsm,
                                                                             current.getParse(),
                                                                             current.getMetamorphicParse(),
                                                                             next.getParse(),
                                                                             next.getMetamorphicParse(),
                                                                             two_next.getParse(),
                                                                             two_next.getMetamorphicParse())
                    if len(literals) > 0:
                        best_synset = self.mostFrequent(literals)
                        if best_synset is not None:
                            current.setSemantic(best_synset.getId())
                            done = True
                            continue
                if previous is not None and isinstance(previous, AnnotatedWord) and previous.getParse() is not None:
                    literals = self.__turkish_wordnet.constructIdiomLiterals(self.__fsm,
                                                                             previous.getParse(),
                                                                             previous.getMetamorphicParse(),
                                                                             current.getParse(),
                                                                             current.getMetamorphicParse())
                    if len(literals) > 0:
                        best_synset = self.mostFrequent(literals)
                        if best_synset is not None:
                            current.setSemantic(best_synset.getId())
                            done = True
                            continue
                if next is not None and isinstance(next, AnnotatedWord) and next.getParse() is not None:
                    literals = self.__turkish_wordnet.constructIdiomLiterals(self.__fsm,
                                                                             current.getParse(),
                                                                             current.getMetamorphicParse(),
                                                                             next.getParse(),
                                                                             next.getMetamorphicParse())
                    if len(literals) > 0:
                        best_synset = self.mostFrequent(literals)
                        if best_synset is not None:
                            current.setSemantic(best_synset.getId())
                            done = True
                            continue
                literals = self.__turkish_wordnet.constructLiterals(current.getParse().getWord().getName(),
                                                                    current.getParse(),
                                                                    current.getMetamorphicParse(),
                                                                    self.__fsm)
                if current.getSemantic() is None and len(literals) > 0:
                    best_synset = self.mostFrequent(literals)
                    if best_synset is not None:
                        current.setSemantic(best_synset.getId())
                        done = True
        return done
