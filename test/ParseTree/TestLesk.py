import unittest

from AnnotatedSentence.AnnotatedWord import ViewLayerType
from AnnotatedTree.Processor.Condition.IsTurkishLeafNode import IsTurkishLeafNode
from AnnotatedTree.Processor.NodeDrawableCollector import NodeDrawableCollector
from AnnotatedTree.TreeBankDrawable import TreeBankDrawable
from MorphologicalAnalysis.FsmMorphologicalAnalyzer import FsmMorphologicalAnalyzer
from WordNet.WordNet import WordNet

from WordSenseDisambiguation.ParseTree.Lesk import Lesk


class TestLesk(unittest.TestCase):

    fsm: FsmMorphologicalAnalyzer
    wordNet: WordNet

    def setUp(self) -> None:
        self.fsm = FsmMorphologicalAnalyzer("../../turkish_dictionary.txt", "../../turkish_misspellings.txt", "../../turkish_finite_state_machine.xml")
        self.wordNet = WordNet("../../turkish_wordnet.xml")

    def test_Accuracy(self):
        correct = 0
        total = 0
        lesk = Lesk(self.wordNet, self.fsm)
        treeBank1 = TreeBankDrawable("../../new-trees")
        treeBank2 = TreeBankDrawable("../../old-trees")
        for i in range(treeBank1.size()):
            parseTree1 = treeBank1.get(i)
            parseTree2 = treeBank2.get(i)
            lesk.autoSemantic(parseTree1)
            nodeDrawableCollector1 = NodeDrawableCollector(parseTree1.getRoot(), IsTurkishLeafNode())
            leafList1 = nodeDrawableCollector1.collect()
            nodeDrawableCollector2 = NodeDrawableCollector(parseTree2.getRoot(), IsTurkishLeafNode())
            leafList2 = nodeDrawableCollector2.collect()
            for j in range(len(leafList1)):
                total = total + 1
                parseNode1 = leafList1[j]
                parseNode2 = leafList2[j]
                if parseNode1.getLayerData(ViewLayerType.SEMANTICS) is not None and parseNode1.getLayerData(ViewLayerType.SEMANTICS) == parseNode2.getLayerData(ViewLayerType.SEMANTICS):
                    correct = correct + 1
        self.assertEqual(475, total)
        self.assertEqual(252, correct)


if __name__ == '__main__':
    unittest.main()
