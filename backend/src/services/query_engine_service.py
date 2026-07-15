from sqlalchemy.orm import Session

from src.services.query_normalizer import normalize_query
from src.services.intent_service import detect_intent
from src.services.nlp_service import lemmatize_text
from src.services.retrieval_service import retrieve_kb_candidates
from src.services.ai_answer_service import generate_grounded_answer


def run_query_engine(
    db: Session,
    raw_query: str,
    department_key: str = "software_engineering",
):
    normalized_query = normalize_query(raw_query)
    lemmatized_query = lemmatize_text(normalized_query)
    intent = detect_intent(lemmatized_query)

    candidates = retrieve_kb_candidates(
        db=db,
        normalized_query=lemmatized_query,
        department_key=department_key,
        limit=10,
    )

    if not candidates:
        return {
            "status": "escalated",
            "intent": intent,
            "normalized_query": lemmatized_query,
            "answer": None,
            "confidence": 0.0,
            "matched_kb_id": None,
            "candidates": [],
            "reason": "No KB match found",
        }

    top = candidates[0]
    second = candidates[1] if len(candidates) > 1 else None
    top_score = top["final_score"]
    diff = top_score - second["final_score"] if second else top_score

    answer = generate_grounded_answer(raw_query, candidates)

    should_escalate = False
    reason = None

    if answer.strip() == "NOT_ENOUGH_CONTEXT":
        should_escalate = True
        reason = "Insufficient context from KB"
    elif top_score < 0.55:
        should_escalate = True
        reason = "Low confidence retrieval score"
    elif second and diff < 0.08:
        should_escalate = True
        reason = "Ambiguous match between KB entries"

    if should_escalate:
        return {
            "status": "escalated",
            "intent": intent,
            "normalized_query": lemmatized_query,
            "answer": None,
            "confidence": round(top_score, 4),
            "matched_kb_id": None,
            "candidates": candidates[:3],
            "reason": reason,
        }

    return {
        "status": "answered",
        "intent": intent,
        "normalized_query": lemmatized_query,
        "answer": answer,
        "confidence": round(top_score, 4),
        "matched_kb_id": top["kb_id"],
        "candidates": candidates[:3],
        "reason": None,
    }