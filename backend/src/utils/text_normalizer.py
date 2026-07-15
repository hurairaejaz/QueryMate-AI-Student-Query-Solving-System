# import re

# ROMAN_URDU_MAP = {
#     "se": "software engineering",
#     "outline": "course outline",
#     "kya hai": "",
#     "konsi": "which",
#     "kon si": "which",
#     "semester": "semester",
#     "sem": "semester",
#     "fee refund": "fee refund policy",
#     "transcript": "transcript",
#     "apply": "application process",
#     "kesy": "how",
#     "kesay": "how",
#     "kaise": "how",
#     "krni": "process",
#     "karni": "process",
# }

# try:
#     import spacy
#     try:
#         NLP = spacy.load("en_core_web_sm")
#     except Exception:
#         NLP = None
# except Exception:
#     NLP = None


# def clean_text(text: str) -> str:
#     text = text.lower().strip()
#     text = re.sub(r"\s+", " ", text)
#     return text


# def normalize_query(text: str) -> str:
#     cleaned = clean_text(text)

#     for key, value in ROMAN_URDU_MAP.items():
#         pattern = r"\b" + re.escape(key) + r"\b"
#         cleaned = re.sub(pattern, value, cleaned)

#     cleaned = re.sub(r"\s+", " ", cleaned).strip()
#     return cleaned


# def normalize_for_search(text: str) -> str:
#     cleaned = normalize_query(text)

#     if NLP is None:
#         return cleaned

#     doc = NLP(cleaned)
#     tokens = [
#         token.lemma_
#         for token in doc
#         if not token.is_stop and not token.is_punct and token.lemma_.strip()
#     ]
#     return " ".join(tokens) if tokens else cleaned




import re


ROMAN_URDU_MAP = {
    "kya": "",
    "ki": "",
    "ka": "",
    "hay": "",
    "hai": "",
    "kr": "kar",
    "se": "",
    "outline": "outline",
    "ai": "artificial intelligence",
    "ml": "machine learning",
    "db": "database",
    "fyp": "final year project",
    "fee refund": "fee refund policy",
    "course outline": "outline",
}


INTENT_KEYWORDS = {
    "outline": "course_outline",
    "policy": "policy_query",
    "fee": "fee_query",
    "refund": "fee_query",
    "schedule": "schedule_query",
    "timetable": "timetable_query",
    "prerequisite": "prerequisite_query",
    "contact": "contact_query",
}


def clean_text(text: str) -> str:
    if not text:
        return ""

    text = text.lower().strip()
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def apply_phrase_replacements(text: str) -> str:
    text = text.replace("what is outline of ai", "artificial intelligence outline")
    text = text.replace("ai ki outline", "artificial intelligence outline")
    text = text.replace("outline of ai", "artificial intelligence outline")
    text = text.replace("ai outline", "artificial intelligence outline")
    return text


def apply_token_mapping(text: str) -> str:
    tokens = text.split()
    normalized_tokens = []

    for token in tokens:
        mapped = ROMAN_URDU_MAP.get(token, token)
        if mapped:
            normalized_tokens.extend(mapped.split())

    return " ".join(normalized_tokens)


def normalize_query_text(text: str) -> str:
    text = clean_text(text)
    text = apply_phrase_replacements(text)
    text = apply_token_mapping(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def detect_language_type(text: str) -> str:
    if not text:
        return "unknown"

    text = text.lower()

    roman_urdu_markers = ["kya", "ki", "ka", "hay", "hai", "kab", "kis", "kon", "kesy"]
    english_markers = ["what", "how", "when", "where", "outline", "policy", "course"]

    has_roman_urdu = any(word in text.split() for word in roman_urdu_markers)
    has_english = any(word in text.split() for word in english_markers)

    if has_roman_urdu and has_english:
        return "mixed"
    if has_roman_urdu:
        return "roman_urdu"
    if has_english:
        return "english"
    return "unknown"


def detect_intent_label(normalized_text: str) -> str:
    for keyword, label in INTENT_KEYWORDS.items():
        if keyword in normalized_text:
            return label
    return "general_query"