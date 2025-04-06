import re

class Tokenizer:
    def __init__(self, tokenizer_rules):
        self.punctuation = tokenizer_rules["punctuation"]
        self.pattern = re.compile(tokenizer_rules["word_regex"])

    def tokenize(self, text):
        return self.pattern.findall(text)

    def tokenize_sentences(self, text):
        return re.split(r'[।!?]', text)
