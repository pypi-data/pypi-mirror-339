class Lemmatizer:
    def __init__(self, lemmatizer_rules):
        self.suffixes = lemmatizer_rules["suffixes"]

    def lemmatize(self, word):
        for suffix in self.suffixes:
            if word.endswith(suffix):
                return word[:-len(suffix)]
        return word
