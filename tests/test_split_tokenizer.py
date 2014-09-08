from unittest import TestCase

from spicedham.split_tokenizer import SplitTokenizer


class TestSplitTokenizer(TestCase):
    def test_tokenize(self):
        tokenizer = SplitTokenizer({})
        # Text was chosen because it's a couple lines and includes ?!\n,. etc.
        test_text = """Not a whit, we defy augury; there's a special providence in
        the fall of a sparrow! If it be now, 'tis not to come; if it be
        not to come, will it be now?"""
        expected_text = ["not", "a", "whit", "we", "defy", "augury;",
        "there's", "a", "special", "providence", "in", "the", "fall", "of",
        "a", "sparrow", "if", "it", "be", "now", "'tis", "not", "to", "come;",
        "if", "it", "be", "not", "to", "come", "will", "it", "be", "now"]
        received_text = tokenizer.tokenize(test_text)
        self.assertEqual(received_text, expected_text)
