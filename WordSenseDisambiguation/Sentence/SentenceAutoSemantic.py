from abc import abstractmethod

from AnnotatedSentence.AnnotatedSentence import AnnotatedSentence
from MorphologicalAnalysis.FsmMorphologicalAnalyzer import FsmMorphologicalAnalyzer
from WordNet.WordNet import WordNet


class SentenceAutoSemantic:

    @abstractmethod
    def autoLabelSingleSemantics(self, sentence: AnnotatedSentence):
        """
        The method should set the senses of all words, for which there is only one possible sense.

        PARAMETERS
        ----------
        sentence: AnnotatedSentence
            The sentence for which word sense disambiguation will be determined automatically.
        """
        pass

    def getCandidateSynSets(self, wordNet: WordNet, fsm: FsmMorphologicalAnalyzer, sentence: AnnotatedSentence, index: int) -> list:
        twoPrevious = None
        previous = None
        twoNext = None
        next = None
        current = sentence.getWord(index)
        if index > 1:
            twoPrevious = sentence.getWord(index - 2)
        if index > 0:
            previous = sentence.getWord(index - 1)
        if index != sentence.wordCount() - 1:
            next = sentence.getWord(index + 1)
        if index < sentence.wordCount() - 2:
            twoNext = sentence.getWord(index + 2)
        synSets = wordNet.constructSynSets(current.getParse().getWord().getName(),
                current.getParse(), current.getMetamorphicParse(), fsm)
        if twoPrevious is not None and twoPrevious.getParse() is not None and previous.getParse() is not None:
            synSets.extend(wordNet.constructIdiomSynSets(twoPrevious.getParse(), previous.getParse(), current.getParse(),
                    twoPrevious.getMetamorphicParse(), previous.getMetamorphicParse(), current.getMetamorphicParse(), fsm))
        if previous is not None and previous.getParse() is not None and next is not None and next.getParse() is not None:
            synSets.extend(wordNet.constructIdiomSynSets(previous.getParse(), current.getParse(), next.getParse(),
                    previous.getMetamorphicParse(), current.getMetamorphicParse(), next.getMetamorphicParse(), fsm))
        if next is not None and next.getParse() is not None and twoNext is not None and twoNext.getParse() is not None:
            synSets.extend(wordNet.constructIdiomSynSets(current.getParse(), next.getParse(), twoNext.getParse(),
                    current.getMetamorphicParse(), next.getMetamorphicParse(), twoNext.getMetamorphicParse(), fsm))
        if previous is not None and previous.getParse() is not None:
            synSets.extend(wordNet.constructIdiomSynSets(previous.getParse(), current.getParse(),
                    previous.getMetamorphicParse(), current.getMetamorphicParse(), fsm))
        if next is not None and next.getParse() is not None:
            synSets.extend(wordNet.constructIdiomSynSets(current.getParse(), next.getParse(),
                    current.getMetamorphicParse(), next.getMetamorphicParse(), fsm))
        return synSets

    def autoSemantic(self, sentence: AnnotatedSentence):
        if self.autoLabelSingleSemantics(sentence):
            sentence.save()
