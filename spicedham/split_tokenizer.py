from re import split

from spicedham.tokenizer import BaseTokenizer

class SplitTokenizer(BaseTokenizer):
    """
    Split the text on punctuation and newlines, lowercase everything, and
    filter the empty strings
    """
   
    def tokenize(self, text):
        text = split('[ ,.?!\n\r]', text)
        text = [token.lower() for token in text if token]
        return text
