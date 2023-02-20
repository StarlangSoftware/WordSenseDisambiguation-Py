from random import randrange
import random

from AnnotatedSentence.AnnotatedWord import ViewLayerType
from AnnotatedTree.ParseTreeDrawable import ParseTreeDrawable
from AnnotatedTree.Processor.Condition.IsTurkishLeafNode import IsTurkishLeafNode
from AnnotatedTree.Processor.NodeDrawableCollector import NodeDrawableCollector
from MorphologicalAnalysis.FsmMorphologicalAnalyzer import FsmMorphologicalAnalyzer
from WordNet.SynSet import SynSet
from WordNet.WordNet import WordNet

from WordSenseDisambiguation.ParseTree.TreeAutoSemantic import TreeAutoSemantic


class Lesk(TreeAutoSemantic):

    __turkish_wordnet: WordNet
    __fsm: FsmMorphologicalAnalyzer

    def __init__(self, turkishWordNet: WordNet, fsm: FsmMorphologicalAnalyzer):
        self.__fsm = fsm
        self.__turkish_wordnet = turkishWordNet

    def intersection(self, synSet: SynSet, leafList: list) -> int:
        if synSet.getExample() is not None:
            words1 = (synSet.getLongDefinition() + " " + synSet.getExample()).split(" ")
        else:
            words1 = synSet.getLongDefinition().split(" ")
        words2 = []
        for i in range(len(leafList)):
            words2.append(leafList[i].getLayerData(ViewLayerType.TURKISH_WORD))
        count = 0
        for word1 in words1:
            for word2 in words2:
                if word1.lower() == word2.lower():
                    count = count + 1
        return count

    def autoLabelSingleSemantics(self, parseTree: ParseTreeDrawable) -> bool:
        random.seed(1)
        node_drawable_collector = NodeDrawableCollector(parseTree.getRoot(), IsTurkishLeafNode())
        leaf_list = node_drawable_collector.collect()
        done = False
        for i in range(len(leaf_list)):
            syn_sets = self.getCandidateSynSets(self.__turkish_wordnet, self.__fsm, leaf_list, i)
            max_intersection = -1
            for j in range(len(syn_sets)):
                syn_set = syn_sets[j]
                intersection_count = self.intersection(syn_set, leaf_list)
                if intersection_count > max_intersection:
                    max_intersection = intersection_count
            max_syn_sets = []
            for j in range(len(syn_sets)):
                syn_set = syn_sets[j]
                if self.intersection(syn_set,leaf_list) == max_intersection:
                    max_syn_sets.append(syn_set)
            if len(max_syn_sets) > 0:
                leaf_list[i].getLayerInfo().setLayerData(ViewLayerType.SEMANTICS, max_syn_sets[randrange(len(max_syn_sets))].getId())
                done = True
        return done
