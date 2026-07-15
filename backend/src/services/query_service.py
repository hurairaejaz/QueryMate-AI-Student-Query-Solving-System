# # # from src.ai.ai_validation import validate_and_enhance_answer  # your AI step
# # # from src.services.rag_service import retrieve_kb_context      # your retrieval

# # # def answer_user_query(db, user_question: str, department_id: int | None):
# # #     context = retrieve_kb_context(db, user_question, department_id)

# # #     raw_answer = generate_answer_from_context(context, user_question)  # LLM or template
# # #     final_answer = validate_and_enhance_answer(user_question, raw_answer, context)

# # #     return final_answer

# # import re
# # from sqlalchemy import or_
# # from sqlalchemy.orm import Session
# # from sqlalchemy.sql import func
# # from src.models.query import Query
# # from src.models.response import Response
# # from src.services.ai_services import AIService
# # from src.models.kb_content import KnowledgeBase
# # from src.services.kb_services import search_kb_entries
# # from src.services.rag_services import answer_query_with_rag
# # from src.models.attachements import Attachment

# # def submit_app_query(db: Session, student_user_id: int, query_text: str, department_key: str = "software_engineering"):
# #     # 1. Save incoming query first
# #     query_obj = Query(
# #         query_text=query_text,
# #         source="mobile",
# #         student_user_id=student_user_id,
# #         status="pending",
# #     )
# #     db.add(query_obj)
# #     db.commit()
# #     db.refresh(query_obj)
# #     # 2. Normalize and search KB
# #     normalized = AIService.normalize(query_text)
# #     kb_rows = search_kb_entries(db, department_key, normalized)
# #     ai_answer = AIService.build_answer_from_kb(query_text, kb_rows)

# #     if ai_answer:
# #         query_obj.ai_response = ai_answer
# #         query_obj.status = "answered"
# #         query_obj.updated_at = func.now()
# #         db.add(
# #             Response(
# #                 query_id=query_obj.query_id,
# #                 responder_id=None,
# #                 response_text=ai_answer,
# #             )
# #         )
# #     else:
# #         query_obj.ai_response = None
# #         query_obj.status = "escalated"
# #         query_obj.updated_at = func.now()

# #     db.commit()
# #     db.refresh(query_obj)
# #     return query_obj


# # def submit_whatsapp_query(
# #     db: Session,
# #     whatsapp_user_id: int,
# #     query_text: str,
# #     department_key: str = "software_engineering",
# # ):
# #     query_obj = Query(
# #         query_text=query_text,
# #         source="whatsapp",
# #         whatsapp_user_id=whatsapp_user_id,
# #         status="pending",
# #     )
# #     db.add(query_obj)
# #     db.commit()
# #     db.refresh(query_obj)

# #     normalized = AIService.normalize(query_text)
# #     kb_rows = search_kb_entries(db, department_key, normalized)
# #     ai_answer = AIService.build_answer_from_kb(query_text, kb_rows)

# #     if ai_answer:
# #         query_obj.ai_response = ai_answer
# #         query_obj.status = "answered"
# #         query_obj.updated_at = func.now()
# #         db.add(
# #             Response(
# #                 query_id=query_obj.query_id,
# #                 responder_id=None,
# #                 response_text=ai_answer,
# #             )
# #         )
# #     else:
# #         query_obj.ai_response = None
# #         query_obj.status = "escalated"
# #         query_obj.updated_at = func.now()

# #     db.commit()
# #     db.refresh(query_obj)
# #     return query_obj


# # def create_and_answer_query(
# #     db: Session,
# #     query_text: str,
# #     source: str,
# #     student_user_id: int | None = None,
# #     whatsapp_user_id: int | None = None
# # ):
# #     query_obj = Query(
# #         query_text=query_text,
# #         source=source,
# #         student_user_id=student_user_id,
# #         whatsapp_user_id=whatsapp_user_id,
# #         status="pending"
# #     )
# #     db.add(query_obj)
# #     db.commit()
# #     db.refresh(query_obj)

# #     answer, retrieved_chunks = answer_query_with_rag(db, query_text)

# #     query_obj.ai_response = answer
# #     query_obj.status = "answered"
# #     query_obj.updated_at = func.now()

# #     response_obj = Response(
# #         query_id=query_obj.query_id,
# #         responder_id=None,
# #         response_text=answer
# #     )
# #     db.add(response_obj)
# #     db.commit()
# #     db.refresh(query_obj)

# #     return query_obj, retrieved_chunks



# # from src.ai.ai_validation import validate_and_enhance_answer  # your AI step
# # from src.services.rag_service import retrieve_kb_context      # your retrieval

# # def answer_user_query(db, user_question: str, department_id: int | None):
# #     context = retrieve_kb_context(db, user_question, department_id)

# #     raw_answer = generate_answer_from_context(context, user_question)  # LLM or template
# #     final_answer = validate_and_enhance_answer(user_question, raw_answer, context)

# #     return final_answer

# import re
# from sqlalchemy import or_
# from sqlalchemy.orm import Session
# from sqlalchemy.sql import func
# from sqlalchemy import text
# from src.models.query import Query
# from src.models.response import Response
# from src.services.ai_services import AIService
# from src.models.kb_content import KnowledgeBase
# from src.services.kb_services import search_kb_entries
# from src.services.rag_services import answer_query_with_rag
# from src.models.attachements import Attachment
# from src.services.semantic_service import semantic_search_kb


# def normalize_query_text(text: str) -> str:
#     if not text:
#         return ""

#     q = text.strip().lower()

#     # remove special characters
#     q = re.sub(r"[^\w\s]", " ", q)

#     # phrase-level normalization first
#     phrase_replacements = {
#         "kya hay": "",
#         "kya hai": "",
#         "kia hay": "",
#         "kia hai": "",
#         "mujhe": "",
#         "batao": "",
#         "pls": "",
#         "plz": "",
#         "please": "",
#         "course outline": "outline",
#         "syllabus": "outline",
#         "pre requisite": "prerequisite",
#         "pre req": "prerequisite",
#         "fee refund": "fee refund policy",
#         "refund fee": "fee refund policy",
#         "transcript apply": "transcript application",
#         "result card": "transcript",
#         "6th sem": "6th semester",
#         "7th sem": "7th semester",
#         "8th sem": "8th semester",
#     }

#     for old, new in phrase_replacements.items():
#         q = q.replace(old, new)

#     # word-level normalization
#     word_replacements = {
#         "ki": " ",
#         "ka": " ",
#         "ke": " ",
#         "hai": " ",
#         "hay": " ",
#         "ai": "artificial intelligence",
#         "se": "software engineering",
#         "cs": "computer science",
#         "it": "information technology",
#         "oop": "object oriented programming",
#         "dsa": "data structures and algorithms",
#         "db": "database",
#         "sem": "semester",
#     }

#     words = q.split()
#     normalized_words = []

#     for word in words:
#         normalized_words.append(word_replacements.get(word, word))

#     q = " ".join(normalized_words)
#     q = re.sub(r"\s+", " ", q).strip()

#     return q


# def calculate_confidence(query_text: str, kb_title: str, kb_content: str) -> float:
#     query_words = set(re.sub(r"[^\w\s]", " ", query_text.lower()).split())
#     title_words = set(re.sub(r"[^\w\s]", " ", kb_title.lower()).split())
#     content_words = set(re.sub(r"[^\w\s]", " ", kb_content.lower()).split())

#     if not query_words:
#         return 0.0

#     title_overlap = len(query_words.intersection(title_words))
#     content_overlap = len(query_words.intersection(content_words))

#     score = ((title_overlap * 1.5) + content_overlap) / max(len(query_words), 1)

#     full_text = f"{kb_title} {kb_content}".lower()
#     if query_text.lower() in full_text:
#         score += 0.2

#     return round(min(score, 1.0), 2)


# def find_best_kb_match(db: Session, normalized_query: str):
#     if not normalized_query:
#         return None, 0.0

#     sql = text("""
#         SELECT
#             kb_id,
#             title,
#             content,
#             department_key,
#             ts_rank(
#                 search_vector,
#                 websearch_to_tsquery('english', :query)
#             ) AS fts_score,
#             similarity(title, :query) AS title_similarity,
#             similarity(content, :query) AS content_similarity
#         FROM software_engineering.knowledge_base
#         WHERE department_key = 'software_engineering'
#           AND (
#                 search_vector @@ websearch_to_tsquery('english', :query)
#                 OR similarity(title, :query) > 0.08
#                 OR similarity(content, :query) > 0.08
#                 OR title ILIKE :like_query
#                 OR content ILIKE :like_query
#           )
#         ORDER BY
#             ts_rank(search_vector, websearch_to_tsquery('english', :query)) DESC,
#             similarity(title, :query) DESC,
#             similarity(content, :query) DESC
#         LIMIT 5
#     """)

#     rows = db.execute(sql, {
#         "query": normalized_query,
#         "like_query": f"%{normalized_query}%"
#     }).mappings().all()

#     if not rows:
#         return None, 0.0

#     best_row = rows[0]
#     matched_kb = (
#         db.query(KnowledgeBase)
#         .filter(KnowledgeBase.kb_id == best_row["kb_id"])
#         .first()
#     )

#     if not matched_kb:
#         return None, 0.0

#     fts_score = float(best_row["fts_score"] or 0.0)
#     title_similarity = float(best_row["title_similarity"] or 0.0)
#     content_similarity = float(best_row["content_similarity"] or 0.0)

#     confidence_score = (
#         0.5 * fts_score +
#         0.3 * title_similarity +
#         0.2 * content_similarity
#     )

#     if confidence_score > 1:
#         confidence_score = 1.0

#     return matched_kb, round(confidence_score, 2)


# def get_first_attachment(db: Session, kb_id: int):
#     return (
#         db.query(Attachment)
#         .filter(Attachment.kb_id == kb_id)
#         .order_by(Attachment.attachment_id.asc())
#         .all()
#     )


# def submit_app_query(db: Session, student_user_id: int, query_text: str):
#     normalized_query = normalize_query_text(query_text)

#     new_query = Query(
#         student_user_id=student_user_id,
#         query_text=query_text,
#         normalized_query=normalized_query,
#         source="mobile",
#         status="pending",
#     )
#     db.add(new_query)
#     db.commit()
#     db.refresh(new_query)

#     matched_kb = None
#     confidence_score = 0.0

#     # 1. lexical search
#     lexical_kb, lexical_score = find_best_kb_match(db, normalized_query)

#     if lexical_kb and lexical_score >= 0.08:
#         matched_kb = lexical_kb
#         confidence_score = lexical_score

#     # 2. semantic fallback
#     if matched_kb is None:
#         semantic_results = semantic_search_kb(
#             db=db,
#             query_text=normalized_query,
#             department_key="software_engineering",
#             top_k=5,
#         )

#         if semantic_results:
#             top_semantic = semantic_results[0]
#             semantic_kb = top_semantic["kb"]
#             semantic_score = top_semantic["semantic_score"]

#             if semantic_score >= 0.45:
#                 matched_kb = semantic_kb
#                 confidence_score = round(semantic_score, 2)

#     # 3. if match found → answer + document
#     if matched_kb:
#         attachment = get_first_attachment(db, matched_kb.kb_id)

#         answer_text = matched_kb.content

#         try:
#             ai_answer = AIService.build_answer_from_kb(query_text, [matched_kb])
#             if ai_answer and str(ai_answer).strip():
#                 answer_text = str(ai_answer).strip()
#         except Exception as e:
#             print("AIService error:", e)

#         new_query.status = "answered"
#         new_query.ai_response = answer_text
#         new_query.confidence_score = confidence_score
#         new_query.matched_kb_id = matched_kb.kb_id

#         response_row = Response(
#             query_id=new_query.query_id,
#             response_text=answer_text,
#             response_source="ai",
#             document_name=attachment.file_name if attachment else None,
#             document_url=f"/app/query/document/{attachment.attachment_id}" if attachment else None,
#         )
#         db.add(response_row)
#         db.commit()
#         db.refresh(new_query)

#         return {
#             "query_id": new_query.query_id,
#             "status": new_query.status,
#             "answer": answer_text,
#             "confidence_score": confidence_score,
#             "matched_kb_id": matched_kb.kb_id,
#            "document": {
#                "attachment_id": attachment.attachment_id,
#                "file_name": attachment.file_name,
#                "file_url": attachment.file_url,
#                "open_url": f"/app/query/document/{attachment.attachment_id}",
#                "mime_type": attachment.mime_type,
#            } if attachment else None,
#             "message": "Answer generated successfully."
#         }

#     # 4. if no match → escalate
#     new_query.status = "escalated"
#     new_query.confidence_score = confidence_score
#     db.commit()
#     db.refresh(new_query)

#     return {
#         "query_id": new_query.query_id,
#         "status": new_query.status,
#         "answer": None,
#         "confidence_score": confidence_score,
#         "matched_kb_id": None,
#         "document": None,
#         "message": "No good match found. Query has been escalated."
#     }

    

# def get_student_query_history(db: Session, student_user_id: int):
#     queries = (
#         db.query(Query)
#         .filter(Query.student_user_id == student_user_id)
#         .order_by(Query.created_at.desc())
#         .all()
#     )
#     return queries




import re
from sqlalchemy.orm import Session
from sqlalchemy import text
from src.models.user import Users
from src.models.query import Query
from src.models.response import Response
from src.models.kb_chunks import KBChunk
from src.models.query_event import QueryEvent
from src.models.kb_content import KnowledgeBase
from src.models.attachements import Attachment

from src.services.ai_services import AIService
from src.services.semantic_service import semantic_search_kb
MIN_LEXICAL_CONFIDENCE = 0.40
MIN_SEMANTIC_CONFIDENCE = 0.45

def normalize_query_text(text_value: str) -> str:
    if not text_value:
        return ""

    q = text_value.strip().lower()

    q = re.sub(r"[^\w\s]", " ", q)

    phrase_replacements = {
        "kya hay": "",
        "kya hai": "",
        "kia hay": "",
        "kia hai": "",
        "mujhe": "",
        "batao": "",
        "pls": "",
        "plz": "",
        "please": "",
        "course outline": "outline",
        "syllabus": "outline",
        "pre requisite": "prerequisite",
        "pre req": "prerequisite",
        "fee refund": "fee refund policy",
        "refund fee": "fee refund policy",
        "transcript apply": "transcript application",
        "result card": "transcript",
        "6th sem": "6th semester",
        "7th sem": "7th semester",
        "8th sem": "8th semester",
        "what is the process of": "process",
        "what is process of": "process",
        "tell me the process of": "process",
        "tell me about": "",
        "what is": "",
        "how to": "process",
        "how can i": "process",

        "course outline": "outline",
        "course outlines": "outline",
        "outlines": "outline",
        "outlineresearch": "outline research",
        "outlinesimulation": "outline simulation",
        "outlinesoftware": "outline software",
        "whatiscourse": "outline",
        "what iscourse": "outline",

        "syllabus": "outline",
        "subject outline": "outline",

        "student id card": "student identity card",
        "duplicate student id card": "duplicate student identity card",
        "noc": "no objection certificate",
        "dmc": "detailed marks certificate",
        "bonafied": "bonafide",
        "bonafide certificate": "bonafide certificate",
        "tution": "tuition",

        "result card": "result card",
        "degree issuaance": "degree issuance",
        "degree issuance": "degree issuance",
        "roll no": "roll number",
        "tcs": "courier tcs",
    }

    for old, new in phrase_replacements.items():
        q = q.replace(old, new)

    word_replacements = {
        "ki": "",
        "ka": "",
        "ke": "",
        "hai": "",
        "hay": "",
        "please": "",
        "pls": "",
        "plz": "",
        "mujhe": "",
        "batao": "",
        "ai": "artificial intelligence",
        "db": "database",
        "dbms": "database system",
        "se": "software engineering",
        "cs": "computer science",
        "it": "information technology",
        "oop": "object oriented programming",
        "os": "operating system",
        "cn": "computer network",
        "hci": "human computer interaction",
        "nlp": "natural language processing",
        "bpe": "business process engineering",
        "pf": "programming fundamental",
        "sqa": "software quality assurance",
        "sre": "software requirement engineering",
        "spm": "software project management",
        "das": "data structures and algorithms",
        "ds":"data science",   
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
        "bonafied": "bonafide certificate process",
        "bonafied certificate": "bonafide certificate process",
        "bonafide certicate": "bonafide certificate process",
        "bonafied certicate": "bonafide certificate process",
        "medium of instruction" : "medium of instruction certificate process",
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

    words = q.split()
    normalized_words = []

    for word in words:
        normalized_words.append(word_replacements.get(word, word))

    q = " ".join(normalized_words)
    q = re.sub(r"\s+", " ", q).strip()

    return q

def build_greeting(source: str, student_name: str | None = None) -> str:
    if source == "mobile":
        name = student_name.strip() if student_name else "Student"
        return f"Hello {name}, "

    if source == "whatsapp":
        return "Hello, "

    return ""


def subject_words_match(query_text: str, kb_title: str, kb_content: str) -> bool:
    query_words = set(re.sub(r"[^\w\s]", " ", query_text.lower()).split())

    stop_words = {
        "what", "are", "is", "the", "of", "a", "an", "in", "on", "for",
        "please", "tell", "me", "show", "give", "details", "detail",
        "process", "procedure", "how", "course", "outline", "syllabus",
        "fee", "charges"
    }

    important_words = query_words - stop_words

    kb_text = f"{kb_title} {kb_content}".lower()

    if not important_words:
        return False

    matched_words = [word for word in important_words if word in kb_text]

    return len(matched_words) >= 1


#  Stricter subject matching to avoid wrong KB answers
def subject_words_match(query_text: str, kb_title: str, kb_content: str) -> bool:
    query_words = set(re.sub(r"[^\w\s]", " ", query_text.lower()).split())

    stop_words = {
        "what", "are", "is", "the", "of", "a", "an", "in", "on", "for",
        "outline", "course", "syllabus", "please", "tell", "me", "show",
        "give", "details", "detail", "process", "procedure", "how"
    }

    important_query_words = query_words - stop_words

    kb_text = f"{kb_title} {kb_content}".lower()

    if not important_query_words:
        return False

    matched_words = [word for word in important_query_words if word in kb_text]

    return len(matched_words) >= max(1, len(important_query_words))

def detect_language_type(text_value: str) -> str:
    if not text_value:
        return "unknown"

    text_value = text_value.lower().strip()
    roman_urdu_markers = {"kya", "ki", "ka", "ke", "hay", "hai", "batao", "mujhe"}
    english_markers = {"what", "how", "outline", "policy", "semester", "course" , "prerequisite" , "refund", "transcript", "timetable", "syllabus", "process", "procedure"}

    words = set(text_value.split())

    has_roman = bool(words.intersection(roman_urdu_markers))
    has_english = bool(words.intersection(english_markers))

    if has_roman and has_english:
        return "mixed"
    if has_roman:
        return "roman_urdu"
    if has_english:
        return "english"
    return "unknown"


def detect_intent_label(normalized_text: str) -> str:
    if not normalized_text:
        return "general_query"

    if "outline" in normalized_text:
        return "course_outline"
    if "prerequisite" in normalized_text:
        return "prerequisite_query"
    if "fee" in normalized_text or "refund" in normalized_text:
        return "fee_query"
    if "transcript" in normalized_text:
        return "transcript_query"
    if "semester" in normalized_text or "timetable" in normalized_text:
        return "semester_query"

    return "general_query"


def create_query_event(
    db: Session,
    query_id: int,
    event_type: str,
    event_message: str | None = None,
    created_by: int | None = None,
) -> None:
    event = QueryEvent(
        query_id=query_id,
        event_type=event_type,
        event_message=event_message,
        created_by=created_by,
    )
    db.add(event)
    db.commit()


def find_best_kb_match(db: Session, normalized_query: str):
    if not normalized_query:
        return None, 0.0

    sql = text("""
        SELECT
            kb_id,
            title,
            content,
            department_key,
            ts_rank(
                search_vector,
                websearch_to_tsquery('english', :query)
            ) AS fts_score,
            similarity(title, :query) AS title_similarity,
            similarity(content, :query) AS content_similarity
        FROM software_engineering.knowledge_base
        WHERE department_key = 'software_engineering'
          AND (
                search_vector @@ websearch_to_tsquery('english', :query)
                OR similarity(title, :query) > 0.20
                OR similarity(content, :query) > 0.20
                OR title ILIKE :like_query
                OR content ILIKE :like_query
          )
        ORDER BY
            ts_rank(search_vector, websearch_to_tsquery('english', :query)) DESC,
            similarity(title, :query) DESC,
            similarity(content, :query) DESC
        LIMIT 1
    """)

    rows = db.execute(sql, {
    "query": normalized_query,
    "like_query": f"%{normalized_query}%"
}).mappings().all()
    if not rows:
        return None, 0.0

    best_row = rows[0]

    fts_score = float(best_row["fts_score"] or 0.0)
    title_similarity = float(best_row["title_similarity"] or 0.0)
    content_similarity = float(best_row["content_similarity"] or 0.0)

    confidence_score = max(
        fts_score,
        title_similarity,
        content_similarity
    )

    if confidence_score < MIN_LEXICAL_CONFIDENCE:
         if normalized_query.lower() not in f"{best_row['title']} {best_row['content']}".lower():
             return None, round(confidence_score, 2)
   
        

    matched_kb = (
        db.query(KnowledgeBase)
        .filter(KnowledgeBase.kb_id == best_row["kb_id"])
        .first()
    )

    if not matched_kb:
        return None, 0.0

    return matched_kb, round(confidence_score, 2)


def search_relevant_chunks(db: Session, normalized_query: str, kb_id: int | None = None, limit: int = 3):
    if not normalized_query:
        return []

    query = db.query(KBChunk)

    if kb_id:
        query = query.filter(KBChunk.kb_id == kb_id)

    terms = normalized_query.split()

    results = []
    chunks = query.all()

    query_words = set(terms)

    for chunk in chunks:
        chunk_words = set(re.sub(r"[^\w\s]", " ", (chunk.chunk_text or "").lower()).split())
        if not chunk_words:
            continue

        overlap = len(query_words.intersection(chunk_words))
        if overlap > 0:
            score = overlap / max(len(query_words), 1)
            results.append({
                "chunk": chunk,
                "score": round(score, 2),
            })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:limit]


def get_first_attachment(db: Session, kb_id: int):
    return (
        db.query(Attachment)
        .filter(Attachment.kb_id == kb_id)
        .order_by(Attachment.attachment_id.asc())
        .first()
    )


def build_document_payload(attachment: Attachment | None):
    if not attachment:
        return None

    return {
        "attachment_id": attachment.attachment_id,
        "file_name": attachment.file_name,
        "file_url": attachment.file_url,
        "open_url": f"/app/query/document/{attachment.attachment_id}",
        "download_url": f"/app/query/document/{attachment.attachment_id}",
        "mime_type": attachment.mime_type,
        "file_type": attachment.file_type,
    }


def submit_app_query(db: Session, student_user_id: int, query_text: str):
    normalized_text = normalize_query_text(query_text)
    detected_language = detect_language_type(query_text)
    intent_label = detect_intent_label(normalized_text)
    student = db.query(Users).filter(Users.user_id == student_user_id).first()
    student_name = student.full_name if student else "Student"
    greeting = build_greeting("mobile", student_name)
    new_query = Query(
        student_user_id=student_user_id,
        query_text=query_text,
        normalized_text=normalized_text,
        detected_language=detected_language,
        intent_label=intent_label,
        source="mobile",
        status="pending",
    )
    db.add(new_query)
    db.commit()
    db.refresh(new_query)

    create_query_event(
        db,
        query_id=new_query.query_id,
        event_type="query_received",
        event_message="Query received from mobile app."
    )

    matched_kb = None
    confidence_score = 0.0

    lexical_kb, lexical_score = find_best_kb_match(db, normalized_text)

    if (
        lexical_kb
        and lexical_score >= MIN_LEXICAL_CONFIDENCE
        and subject_words_match(normalized_text, lexical_kb.title, lexical_kb.content)
     ):
        matched_kb = lexical_kb
        confidence_score = lexical_score

    if matched_kb is None:
        semantic_results = semantic_search_kb(
            db=db,
            query_text=normalized_text,
            department_key="software_engineering",
            top_k=5,
        )

        if semantic_results:
            top_semantic = semantic_results[0]
            semantic_kb = top_semantic["kb"]
            semantic_score = top_semantic["semantic_score"]

            if (
                semantic_score >= MIN_SEMANTIC_CONFIDENCE
                and subject_words_match(normalized_text, semantic_kb.title, semantic_kb.content)
            ):
                matched_kb = semantic_kb
                confidence_score = round(semantic_score, 2)

    if matched_kb:
        chunk_results = search_relevant_chunks(db, normalized_text, kb_id=matched_kb.kb_id, limit=2)
        attachment = get_first_attachment(db, matched_kb.kb_id)

        answer_text =greeting + matched_kb.content.strip()

        if chunk_results:
            top_chunk_text = chunk_results[0]["chunk"].chunk_text.strip()
            answer_text = f"{answer_text}\n\nRelevant document detail: {top_chunk_text[:350]}"

        try:
            ai_answer = AIService.build_answer_from_kb(query_text, [matched_kb])
            if ai_answer and str(ai_answer).strip():
                if chunk_results:
                    answer_text = f"{greeting}{str(ai_answer).strip()}\n\nRelevant document detail: {chunk_results[0]['chunk'].chunk_text[:350].strip()}"
                else:
                    answer_text = greeting + str(ai_answer).strip()
        except Exception as e:
            print("AIService error:", e)

        new_query.status = "answered"
        new_query.ai_response = answer_text
        new_query.confidence_score = confidence_score
        new_query.matched_kb_id = matched_kb.kb_id
        new_query.matched_attachment_id = attachment.attachment_id if attachment else None
        new_query.resolution_type = "ai"

        response_row = Response(
            query_id=new_query.query_id,
            response_text=answer_text,
            response_type="ai",
            responder_id=None,
            confidence_score=confidence_score,
            tone_used="natural" if detected_language in ["roman_urdu", "mixed"] else "formal",
            source_evidence=f"KB:{matched_kb.title}",
            attachment_id=attachment.attachment_id if attachment else None,
        )
        db.add(response_row)
        db.commit()
        db.refresh(new_query)

        create_query_event(
            db,
            query_id=new_query.query_id,
            event_type="ai_answered",
            event_message="AI answer generated successfully."
        )

        return {
            "query_id": new_query.query_id,
            "status": new_query.status,
            "answer": answer_text,
            "confidence_score": confidence_score,
            "matched_kb_id": matched_kb.kb_id,
            "documents": [build_document_payload(attachment)] if attachment else [],
            "message": "Answer generated successfully."
        }

    new_query.status = "escalated"
    new_query.confidence_score = confidence_score
    new_query.escalation_reason = "No good KB or chunk match found."
    db.commit()
    db.refresh(new_query)

    create_query_event(
        db,
        query_id=new_query.query_id,
        event_type="escalated",
        event_message="No reliable answer found. Query escalated."
    )

    return {
        "query_id": new_query.query_id,
        "status": new_query.status,
        "answer": None,
        "confidence_score": confidence_score,
        "matched_kb_id": None,
        "documents": [],
        "message": "Unfortunately, our database does not have a reliable answer to your question at that moment. Your query has been escalated to our support team, and they will get back to you as soon as possible. We apologize for the inconvenience. Thank you for your understanding.❤️"
    }


def submit_whatsapp_query(db: Session, whatsapp_user_id: int, query_text: str):
    normalized_text = normalize_query_text(query_text)
    detected_language = detect_language_type(query_text)
    intent_label = detect_intent_label(normalized_text)

    new_query = Query(
        whatsapp_user_id=whatsapp_user_id,
        query_text=query_text,
        normalized_text=normalized_text,
        detected_language=detected_language,
        intent_label=intent_label,
        source="whatsapp",
        status="pending",
    )
    db.add(new_query)
    db.commit()
    db.refresh(new_query)

    create_query_event(
        db,
        query_id=new_query.query_id,
        event_type="query_received",
        event_message="Query received from WhatsApp."
    )

    result = submit_query_common_flow(db=db, query_obj=new_query)
    return result


def submit_query_common_flow(db: Session, query_obj: Query):
    normalized_text = query_obj.normalized_text or normalize_query_text(query_obj.query_text)
    greeting = build_greeting(query_obj.source)
    matched_kb = None
    confidence_score = 0.0

    lexical_kb, lexical_score = find_best_kb_match(db, normalized_text)

    if (
        lexical_kb
        and lexical_score >= MIN_LEXICAL_CONFIDENCE
        and subject_words_match(normalized_text, lexical_kb.title, lexical_kb.content)
    ):
        matched_kb = lexical_kb
        confidence_score = lexical_score

    if matched_kb is None:
        semantic_results = semantic_search_kb(
            db=db,
            query_text=normalized_text,
            department_key="software_engineering",
            top_k=5,
        )
        if semantic_results:
            top_semantic = semantic_results[0]
            semantic_kb = top_semantic["kb"]
            semantic_score = top_semantic["semantic_score"]

            if (
                semantic_score >= MIN_SEMANTIC_CONFIDENCE
                and subject_words_match(normalized_text, semantic_kb.title, semantic_kb.content)
            ):
                matched_kb = semantic_kb
                confidence_score = round(semantic_score, 2)

    if matched_kb:
        chunk_results = search_relevant_chunks(db, normalized_text, kb_id=matched_kb.kb_id, limit=2)
        attachment = get_first_attachment(db, matched_kb.kb_id)

        answer_text = greeting + matched_kb.content.strip()

        try:
            ai_answer = AIService.build_answer_from_kb(query_obj.query_text, [matched_kb])
            if ai_answer and str(ai_answer).strip():
                answer_text = greeting + str(ai_answer).strip()
        except Exception as e:
            print("AIService error:", e)

        if chunk_results:
            answer_text = f"{answer_text}\n\nRelevant document detail: {chunk_results[0]['chunk'].chunk_text[:350].strip()}"

        query_obj.status = "answered"
        query_obj.ai_response = answer_text
        query_obj.confidence_score = confidence_score
        query_obj.matched_kb_id = matched_kb.kb_id
        query_obj.matched_attachment_id = attachment.attachment_id if attachment else None
        query_obj.resolution_type = "ai"

        db.add(Response(
            query_id=query_obj.query_id,
            response_text=answer_text,
            response_type="ai",
            responder_id=None,
            confidence_score=confidence_score,
            tone_used="natural" if query_obj.detected_language in ["roman_urdu", "mixed"] else "formal",
            source_evidence=f"KB:{matched_kb.title}",
            attachment_id=attachment.attachment_id if attachment else None,
        ))
        db.commit()
        db.refresh(query_obj)

        create_query_event(
            db,
            query_id=query_obj.query_id,
            event_type="ai_answered",
            event_message="AI answer generated successfully."
        )

        return {
            "query_id": query_obj.query_id,
            "status": query_obj.status,
            "answer": answer_text,
            "confidence_score": confidence_score,
            "matched_kb_id": matched_kb.kb_id,
            "documents": [build_document_payload(attachment)] if attachment else [],
            "message": "Answer generated successfully."
        }

    query_obj.status = "escalated"
    query_obj.confidence_score = confidence_score
    query_obj.escalation_reason = "No good KB or chunk match found."
    db.commit()
    db.refresh(query_obj)

    create_query_event(
        db,
        query_id=query_obj.query_id,
        event_type="escalated",
        event_message="No reliable answer found. Query escalated."
    )

    return {
        "query_id": query_obj.query_id,
        "status": query_obj.status,
        "answer": None,
        "confidence_score": confidence_score,
        "matched_kb_id": None,
        "documents": [],
        "message": "No good match found. Query has been escalated."
    }


def get_student_query_history(db: Session, student_user_id: int):
    queries = (
        db.query(Query,Response)
        .join(Response, Response.query_id == Query.query_id)
        .filter(Query.student_user_id == student_user_id)
        .order_by(Query.created_at.desc())
        .all()
    )
    return queries