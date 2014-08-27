from unittest import TestCase

from spicedham.nonsensefilter import NonsenseFilter

class TestNonsenseFilter(TestCase):
    
    # TODO: This test will likely fail spectacularly because of a lack of
    # training.
    def test_classify(self):
        nonsense = NonsenseFilter()
        nonsense.filter_match = 1
        nonsense.filter_miss = 0
        reverse = lambda x: x[::-1]
        match_message = map(reverse, ['supposedly', 'nonsense', 'words'])
        miss_message = ['Firefox']
        self.assertEqual(nonsense.classify('tag', match_message), 1)
        self.assertEqual(nonsense.classify('tag', miss_message), 0)

