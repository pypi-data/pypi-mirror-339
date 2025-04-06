class POSTagger:
    def __init__(self, pos_rules):
        self.pos_rules = pos_rules["rules"]

    def tag(self, tokens):
        tags = []
        for token in tokens:
            assigned_tag = 'X'  # Default for unknown tokens
            for pos, words in self.pos_rules.items():
                if token in words:
                    assigned_tag = pos
                    break
            tags.append(assigned_tag)
        return tags
