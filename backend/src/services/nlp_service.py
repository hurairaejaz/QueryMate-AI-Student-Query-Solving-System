import spacy

nlp = spacy.load("en_core_web_sm")

def lemmatize_text(text: str) -> str:
    doc = nlp(text)
    tokens = []

    for token in doc:
        if not token.is_space and not token.is_punct:
            lemma = token.lemma_.strip().lower()
            if lemma:
                tokens.append(lemma)

    return " ".join(tokens)