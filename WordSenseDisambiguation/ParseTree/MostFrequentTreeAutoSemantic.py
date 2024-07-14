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
        """
        Constructor for the {@link MostFrequentTreeAutoSemantic} class. Gets the Turkish wordnet and Turkish fst based
        morphological analyzer from the user and sets the corresponding attributes.
        :param turkishWordNet: Turkish wordnet
        :param fsm: Turkish morphological analyzer
        """
        self.__fsm = fsm
        self.__turkish_wordnet = turkishWordNet

    def mostFrequent(self, synSets: list, root: str) -> SynSet:
        """
        Returns the most frequent root word in the given synsets. In the wordnet, literals are ordered and indexed
        according to their usage. The most frequently used sense of the literal has sense number 1, then 2, etc. In order
        to get literal from root word, the algorithm checks root for a prefix and suffix. So, if the root is a prefix or
        suffix of a literal, it is included in the search.
        :param synSets: All possible synsets to search for most frequent literal.
        :param root: Root word to be checked.
        :return: Synset storing most frequent literal either starting or ending with the given root form.
        """
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
        """
        The method annotates the word senses of the words in the parse tree according to the baseline most frequent
        algorithm. The algorithm processes target words one by one. First, the algorithm constructs an array of
        all possible senses for the target word to annotate. Then the sense with the minimum sense index is selected. In
        the wordnet, literals are ordered and indexed according to their usage. The most frequently used sense of the
        literal has sense number 1, then 2, etc.
        :param parseTree: Parse tree to be annotated.
        :return: True, if at least one word is semantically annotated, false otherwise.
        """
        node_drawable_collector = NodeDrawableCollector(parseTree.getRoot(), IsTurkishLeafNode())
        leaf_list = node_drawable_collector.collect()
        for i in range(len(leaf_list)):
            syn_sets = self.getCandidateSynSets(self.__turkish_wordnet, self.__fsm, leaf_list, i)
            if len(syn_sets) > 0:
                best = self.mostFrequent(syn_sets, leaf_list[i].getLayerInfo().getMorphologicalParseAt(0).getWord().getName())
                if best is not None:
                    leaf_list[i].getLayerInfo().setLayerData(ViewLayerType.SEMANTICS, best.getId())
        return True
