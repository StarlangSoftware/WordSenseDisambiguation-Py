import unittest

from AnnotatedSentence.AnnotatedCorpus import AnnotatedCorpus
from MorphologicalAnalysis.FsmMorphologicalAnalyzer import FsmMorphologicalAnalyzer
from WordNet.WordNet import WordNet

from WordSenseDisambiguation.Sentence.Lesk import Lesk


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
        corpus1 = AnnotatedCorpus("../../new-sentences")
        corpus2 = AnnotatedCorpus("../../old-sentences")
        for i in range(corpus1.sentenceCount()):
            sentence1 = corpus1.getSentence(i)
            lesk.autoSemantic(sentence1)
            sentence2 = corpus2.getSentence(i)
            for j in range(sentence1.wordCount()):
                total = total + 1
                word1 = sentence1.getWord(j)
                word2 = sentence2.getWord(j)
                if word1.getSemantic() is not None and word1.getSemantic() == word2.getSemantic():
                    correct = correct + 1
        self.assertEqual(549, total)
        self.assertEqual(258, correct)


if __name__ == '__main__':
    unittest.main()
