import re

ROMAN_URDU_MAP = {
    "kya hai": "",
    "kya hay": "",
    "kia hai": "",
    "kia hay": "",
    "batao": "",
    "mujhe": "",
    "please": "",
    "plz": "",
    "ka": " ",
    "ki": " ",
    "ke": " ",
    "hai": " ",
    "hay": " ",
    "krna": "karna",
    "apply krna": "apply karna",
    "kon se": "which",
    "kaise": "how",
}

DOMAIN_MAP = {
    "ai": "artificial intelligence",
    "se": "software engineering",
    "cs": "computer science",
    "it": "information technology",
    "fyp": "final year project",
    "oop": "object oriented programming",
    "dsa": "data structures and algorithms",
    "db": "database",
    "bpe": "bussiness process engineering",
    "CCE": "civic and community engagement",
    "ds": "data science",
    "dld": "digital logic design",
    "hci": "human-computer interaction",
    "ict": "information and communication technology",
    "mad": "mobile application development",
    "mat": "mobile application technology",
    "nlp": "natural language processing",
    "os": "operating systems",
    "or": "operations research",
    "pom": "principles of marketing",
    "rm": "reasearch methodology",
    "scd": "software construction and development",
    "sda": "softeware design and architecture",
    "see": "software engineering economics",
    "spm": "software project management",
    "sqe": "software quality engineering",
    "Sre": "software requirements engineering",
    "sree": "software re engineering",
    "outline": "course outline",
    "syllabus": "course outline",
    "course content": "course outline",
    "pre req": "prerequisite",
    "pre requisite": "prerequisite",
    "fee refund": "fee refund policy",
    "refund fee": "fee refund policy",
    "refund": "refund policy",
    "transcript apply": "transcript application process",
    "result card": "transcript",
    "admit card": "admit card",
    "challan": "fee challan",
    "semester": "semester",
    "sem": "semester",
    "student registration card": "student registration card process",
    "duplicate student id card": "duplicate student id card process",
    "appeal fee": "appeal fee process",
    "noc": "noc process",
    "noc tcs": "noc with tcs process",
    "character certificate": "character certificate process",
    "student registration fee": "student registration fee process",
    "fine": "fine process",
    "internship letter": "internship letter process",
    "duplicate result card": "duplicate result card process",
    "transcript verification": "transcript verification letter fee process",
    "urgent degree": "urgent degree issuance fee process",
    "special exam centre": "special examination centre process",
    "change of centre": "change of centre process",
    "roll no correction": "correction in roll no process",
    "duplicate degree": "duplicate degree fee process",
    "postal fee": "postal fee process",
    "subject change": "subject change process",
    "proficiency certificate": "proficiency certificate process",
    "bonafide certificate": "bonafide certificate process",
    "medium of instruction": "medium of instruction certificate process",
    "provisional transcript": "provisional transcript process",
    "paper rechecking": "paper rechecking process",
    "degree verification": "degree verification letter fee process",
    "dmc": "dmc process",
    "name correction": "name correction process",
    "misc charges": "miscellaneous charges process",
    "disciplinary committee": "disciplinary committee process",
    "change in particular": "change in particular process",
    "revised transcript": "revised transcript process",
    "result card verification": "verification result card fee process",
    "degree completion letter": "degree completion letter process",
    "transport fee": "transport fee process",
    "provisional certificate": "provisional certificate fee process",
    "final transcript": "final transcript process",
    "merit certificate": "merit certificate process",
    "verified degree copy": "fee for verified copy of degree process",
    "duplicate merit certificate": "duplicate merit certificate fee process",
    "merit certificate verification": "verification merit certificate fee process",
    "backlog certificate": "backlog certificate process",
    "transport charges": "transport charges process",
    "alumni dinner": "alumni dinner convocation process",
    "tuition fee excess": "tuition fee excess return process",
    "revised result card": "revised result card process",
    "proctorial board": "proctorial board process",
    "traffic violation": "traffic violation process",
    "tuition fee recovery": "recovery of tuition fee process",
    "transport fee recovery": "recovery of transport fee process"
}

STOP_PHRASES = [
    "ki outline",
    "ka outline",
    "course ki outline",
    "subject ki outline",
]


def normalize_query(text: str) -> str:
    if not text:
        return ""

    q = text.lower().strip()

    q = re.sub(r"[^\w\s]", " ", q)
    q = re.sub(r"\s+", " ", q).strip()

    for old, new in ROMAN_URDU_MAP.items():
        q = q.replace(old, new)

    q = re.sub(r"\s+", " ", q).strip()

    # phrase replacements first
    phrase_keys = sorted(DOMAIN_MAP.keys(), key=len, reverse=True)
    for old in phrase_keys:
        q = q.replace(old, DOMAIN_MAP[old])

    for phrase in STOP_PHRASES:
        q = q.replace(phrase, " course outline ")

    q = re.sub(r"\s+", " ", q).strip()

    return q