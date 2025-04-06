from .tokenizer import Tokenizer
from .pos_tagger import POSTagger
from .lemmatizer import Lemmatizer
from .ner import NER
from .parser import DependencyParser
from .text_classifier import TextClassifier

class ZNLP:
    def __init__(self, language='bangla', rules_file='resources/rules.json'):
        with open(rules_file, 'r', encoding='utf-8') as f:
            self.rules = json.load(f)
        
        self.language = language if language in self.rules["languages"] else 'bangla'
        language_rules = self.rules["languages"][self.language]
        
        self.tokenizer = Tokenizer(language_rules["tokenizer"])
        self.pos_tagger = POSTagger(language_rules["pos_tagger"])
        self.lemmatizer = Lemmatizer(language_rules["lemmatizer"])
        self.ner = NER(language_rules["ner"])
        self.parser = DependencyParser(language_rules.get("parser", {}))
        self.text_classifier = TextClassifier(language_rules.get("classifier", {}))

    def __call__(self, text):
        tokens = self.tokenizer.tokenize(text)
        pos_tags = self.pos_tagger.tag(tokens)
        lemmas = [self.lemmatizer.lemmatize(token) for token in tokens]
        entities = self.ner.predict(tokens)
        dependencies = self.parser.parse(tokens)
        classification = self.text_classifier.classify(text)
        return ZNLPDoc(tokens, pos_tags, lemmas, entities, dependencies, classification)


class ZNLPDoc:
    def __init__(self, tokens, pos_tags, lemmas, entities, dependencies, classification):
        self.tokens = [ZNLPToken(t, p, l, e) for t, p, l, e in zip(tokens, pos_tags, lemmas, entities)]
        self.dependencies = dependencies
        self.classification = classification

    def __repr__(self):
        return f"ZNLPDoc(Tokens: {len(self.tokens)}, Dependencies: {len(self.dependencies)})"


class ZNLPToken:
    def __init__(self, text, pos, lemma, entity):
        self.text = text
        self.pos = pos
        self.lemma = lemma
        self.entity = entity

    def __repr__(self):
        return f"{self.text} ({self.pos}, {self.lemma}, {self.entity})"
