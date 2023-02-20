from abc import abstractmethod

from AnnotatedTree.ParseTreeDrawable import ParseTreeDrawable
from MorphologicalAnalysis.FsmMorphologicalAnalyzer import FsmMorphologicalAnalyzer
from WordNet.WordNet import WordNet


class TreeAutoSemantic:

    @abstractmethod
    def autoLabelSingleSemantics(self, parseTree: ParseTreeDrawable) -> bool:
        pass

    def getCandidateSynSets(self,
                            wordNet: WordNet,
                            fsm: FsmMorphologicalAnalyzer,
                            leafList: list,
                            index: int) -> list:
        two_previous = None
        previous = None
        two_next = None
        next = None
        current = leafList[index].getLayerInfo()
        if index > 1:
            two_previous = leafList[index - 2].getLayerInfo()
        if index > 0:
            previous = leafList[index - 1].getLayerInfo()
        if index != len(leafList) - 1:
            next = leafList[index + 1].getLayerInfo()
        if index < len(leafList) - 2:
            two_next = leafList[index + 2].getLayerInfo()
        syn_sets = wordNet.constructSynSets(current.getMorphologicalParseAt(0).getWord().getName(),
                    current.getMorphologicalParseAt(0), current.getMetamorphicParseAt(0), fsm)
        if two_previous is not None and two_previous.getMorphologicalParseAt(0) is not None and previous.getMorphologicalParseAt(0) is not None:
            syn_sets.extend(wordNet.constructIdiomSynSets(fsm, two_previous.getMorphologicalParseAt(0), two_previous.getMetamorphicParseAt(0),
                                                         previous.getMorphologicalParseAt(0), previous.getMetamorphicParseAt(0),
                                                         current.getMorphologicalParseAt(0), current.getMetamorphicParseAt(0)))
        if previous is not None and previous.getMorphologicalParseAt(0) is not None and next is not None and next.getMorphologicalParseAt(0) is not None:
            syn_sets.extend(wordNet.constructIdiomSynSets(fsm, previous.getMorphologicalParseAt(0), previous.getMetamorphicParseAt(0),
                                                         current.getMorphologicalParseAt(0), current.getMetamorphicParseAt(0),
                                                         next.getMorphologicalParseAt(0), next.getMetamorphicParseAt(0)))
        if next is not None and next.getMorphologicalParseAt(0) is not None and two_next is not None and two_next.getMorphologicalParseAt(0) is not None:
            syn_sets.extend(wordNet.constructIdiomSynSets(fsm, current.getMorphologicalParseAt(0), current.getMetamorphicParseAt(0),
                                                         next.getMorphologicalParseAt(0), next.getMetamorphicParseAt(0),
                                                         two_next.getMorphologicalParseAt(0), two_next.getMetamorphicParseAt(0)))
        if previous is not None and previous.getMorphologicalParseAt(0) is not None:
            syn_sets.extend(wordNet.constructIdiomSynSets(fsm, previous.getMorphologicalParseAt(0), previous.getMetamorphicParseAt(0),
                                                         current.getMorphologicalParseAt(0), current.getMetamorphicParseAt(0)))
        if next is not None and next.getMorphologicalParseAt(0) is not None:
            syn_sets.extend(wordNet.constructIdiomSynSets(fsm, current.getMorphologicalParseAt(0), current.getMetamorphicParseAt(0),
                                                         next.getMorphologicalParseAt(0), next.getMetamorphicParseAt(0)))
        return syn_sets

    def autoSemantic(self, parseTree: ParseTreeDrawable):
        self.autoLabelSingleSemantics(parseTree)
