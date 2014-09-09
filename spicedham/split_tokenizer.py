from re import split

from spicedham.tokenizer import BaseTokenizer

class SplitTokenizer(BaseTokenizer):
    """
    Split the text on punctuation and newlines, lowercase everything, and
    filter the empty strings
    """
   
    def tokenize(self, text):
        text = split('[ ,.?!\n\r]', text)
        is_not_blank = lambda x: x != ''
        text = filter(is_not_blank, text)
        lower_case = lambda x: x.lower()
        text = map(lower_case, text)
        return text
