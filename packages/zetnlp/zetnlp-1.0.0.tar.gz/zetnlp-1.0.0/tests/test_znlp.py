from znlp import ZNLP

def test_bangla():
    nlp = ZNLP(language='bangla')
    doc = nlp("ঢাকায় আজ খুব গরম।")
    for token in doc.tokens:
        print(f"{token.text} => POS: {token.pos}, Lemma: {token.lemma}, Entity: {token.entity}")

def test_english():
    nlp = ZNLP(language='english')
    doc = nlp("The weather is very hot in New York today.")
    for token in doc.tokens:
        print(f"{token.text} => POS: {token.pos}, Lemma: {token.lemma}, Entity: {token.entity}")

test_bangla()
test_english()
