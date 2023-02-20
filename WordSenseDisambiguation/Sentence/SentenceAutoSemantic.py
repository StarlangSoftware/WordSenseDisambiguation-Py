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
        two_previous = None
        previous = None
        two_next = None
        next = None
        current = sentence.getWord(index)
        if index > 1:
            two_previous = sentence.getWord(index - 2)
        if index > 0:
            previous = sentence.getWord(index - 1)
        if index != sentence.wordCount() - 1:
            next = sentence.getWord(index + 1)
        if index < sentence.wordCount() - 2:
            two_next = sentence.getWord(index + 2)
        syn_sets = wordNet.constructSynSets(current.getParse().getWord().getName(),
                current.getParse(), current.getMetamorphicParse(), fsm)
        if two_previous is not None and two_previous.getParse() is not None and previous.getParse() is not None:
            syn_sets.extend(wordNet.constructIdiomSynSets(fsm, two_previous.getParse(), two_previous.getMetamorphicParse(),
                                                         previous.getParse(), previous.getMetamorphicParse(),
                                                         current.getParse(), current.getMetamorphicParse()))
        if previous is not None and previous.getParse() is not None and next is not None and next.getParse() is not None:
            syn_sets.extend(wordNet.constructIdiomSynSets(fsm, previous.getParse(), previous.getMetamorphicParse(),
                                                         current.getParse(), current.getMetamorphicParse(),
                                                         next.getParse(), next.getMetamorphicParse()))
        if next is not None and next.getParse() is not None and two_next is not None and two_next.getParse() is not None:
            syn_sets.extend(wordNet.constructIdiomSynSets(fsm, current.getParse(), current.getMetamorphicParse(),
                                                         next.getParse(), next.getMetamorphicParse(),
                                                         two_next.getParse(), two_next.getMetamorphicParse()))
        if previous is not None and previous.getParse() is not None:
            syn_sets.extend(wordNet.constructIdiomSynSets(fsm, previous.getParse(), previous.getMetamorphicParse(),
                                                         current.getParse(), current.getMetamorphicParse()))
        if next is not None and next.getParse() is not None:
            syn_sets.extend(wordNet.constructIdiomSynSets(fsm, current.getParse(), current.getMetamorphicParse(),
                                                         next.getParse(), next.getMetamorphicParse()))
        return syn_sets

    def autoSemantic(self, sentence: AnnotatedSentence):
        if self.autoLabelSingleSemantics(sentence):
            sentence.save()
