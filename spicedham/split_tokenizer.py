from re import split

from spicedham.tokenizer import BaseTokenizer

class SplitTokenizer(BaseTokenizer):
    
    def tokenize(self, text):
        """
        Split the text on punctuation and newlines, lowercase everything, and
        filter the empty strings
        """
        text = split('[ ,.?!\n\r]', text)
        is_not_blank = lambda x: x != ''
        text = filter(is_not_blank, text)
        lower_case = lambda x: x.lower()
        text = map(lower_case, text)
        return text
