class NER:
    def __init__(self, ner_rules):
        self.locations = ner_rules["locations"]
        self.persons = ner_rules["persons"]
        self.organizations = ner_rules["organizations"]

    def predict(self, tokens):
        entities = []
        for token in tokens:
            if token in self.locations:
                entities.append("LOC")
            elif token in self.persons:
                entities.append("PER")
            elif token in self.organizations:
                entities.append("ORG")
            else:
                entities.append("O")
        return entities
