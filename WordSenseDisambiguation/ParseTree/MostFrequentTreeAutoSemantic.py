from AnnotatedSentence.AnnotatedWord import ViewLayerType
from AnnotatedTree.ParseTreeDrawable import ParseTreeDrawable
from AnnotatedTree.Processor.Condition.IsTurkishLeafNode import IsTurkishLeafNode
from AnnotatedTree.Processor.NodeDrawableCollector import NodeDrawableCollector
from MorphologicalAnalysis.FsmMorphologicalAnalyzer import FsmMorphologicalAnalyzer
from WordNet.SynSet import SynSet
from WordNet.WordNet import WordNet

from WordSenseDisambiguation.ParseTree.TreeAutoSemantic import TreeAutoSemantic


class MostFrequentTreeAutoSemantic(TreeAutoSemantic):

    __turkish_wordnet: WordNet
    __fsm: FsmMorphologicalAnalyzer

    def __init__(self, turkishWordNet: WordNet, fsm: FsmMorphologicalAnalyzer):
        self.__fsm = fsm
        self.__turkish_wordnet = turkishWordNet

    def mostFrequent(self, synSets: list, root: str) -> SynSet:
        if len(synSets) == 1:
            return synSets[0]
        min_sense = 50
        best = None
        for syn_set in synSets:
            for i in range(syn_set.getSynonym().literalSize()):
                if syn_set.getSynonym().getLiteral(i).getName().lower().startswith(root) or syn_set.getSynonym().getLiteral(i).getName().lower().endswith(" " + root):
                    if syn_set.getSynonym().getLiteral(i).getSense() < min_sense:
                        min_sense = syn_set.getSynonym().getLiteral(i).getSense()
                        best = syn_set
        return best

    def autoLabelSingleSemantics(self, parseTree: ParseTreeDrawable) -> bool:
        node_drawable_collector = NodeDrawableCollector(parseTree.getRoot(), IsTurkishLeafNode())
        leaf_list = node_drawable_collector.collect()
        for i in range(len(leaf_list)):
            syn_sets = self.getCandidateSynSets(self.__turkish_wordnet, self.__fsm, leaf_list, i)
            if len(syn_sets) > 0:
                best = self.mostFrequent(syn_sets, leaf_list[i].getLayerInfo().getMorphologicalParseAt(0).getWord().getName())
                if best is not None:
                    leaf_list[i].getLayerInfo().setLayerData(ViewLayerType.SEMANTICS, best.getId())
        return True
