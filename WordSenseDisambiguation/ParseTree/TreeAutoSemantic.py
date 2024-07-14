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
        """
        The method constructs all possible senses for the word at position index in the given parse tree. The method checks
        the previous two words and the current word; the previous, current and next word, current and the next
        two words to add three word multiword sense (that occurs in the Turkish wordnet) to the result list. The
        method then check the previous word and current word; current word and the next word to add a two word multiword
        sense to the result list. Lastly, the method adds all possible senses of the current word to the result list.
        :param wordNet: Turkish wordnet
        :param fsm: Turkish morphological analyzer
        :param leafList: Leaves of the parse tree to be semantically disambiguated.
        :param index: Position of the word to be disambiguated.
        :return: All possible senses for the word at position index in the given parse tree.
        """
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
        """
        The method tries to semantic annotate as many words in the parse tree as possible.
        :param parseTree: Parse tree to be semantically disambiguated.
        """
        self.autoLabelSingleSemantics(parseTree)
