from sqlalchemy.orm import Session
from sqlalchemy import or_

from src.models.kb_content import KnowledgeBase
from src.models.kb_chunks import KBChunk
from src.models.attachements import Attachment


def simple_text_score(query_text: str, target_text: str) -> float:
    """
    Basic token overlap scoring.
    Returns score between 0 and 1.
    """
    if not query_text or not target_text:
        return 0.0

    query_tokens = set(query_text.lower().split())
    target_tokens = set(target_text.lower().split())

    if not query_tokens or not target_tokens:
        return 0.0

    common = query_tokens.intersection(target_tokens)
    return len(common) / max(len(query_tokens), 1)


def search_kb_by_question(db: Session, normalized_text: str, limit: int = 5) -> list[dict]:
    """
    Search KB entries by title/content using basic LIKE + token score.
    """
    if not normalized_text:
        return []

    terms = normalized_text.split()

    filters = []
    for term in terms:
        filters.append(KnowledgeBase.title.ilike(f"%{term}%"))
        filters.append(KnowledgeBase.content.ilike(f"%{term}%"))

    kb_items = (
        db.query(KnowledgeBase)
        .filter(or_(*filters))
        .limit(limit * 3)
        .all()
    )

    scored_items = []
    for item in kb_items:
        combined = f"{item.title or ''} {item.content or ''}"
        score = simple_text_score(normalized_text, combined)

        scored_items.append({
            "kb": item,
            "score": score,
        })

    scored_items.sort(key=lambda x: x["score"], reverse=True)
    return scored_items[:limit]


def search_chunks(db: Session, normalized_text: str, limit: int = 5) -> list[dict]:
    """
    Search stored chunks by basic LIKE + token score.
    """
    if not normalized_text:
        return []

    terms = normalized_text.split()

    filters = []
    for term in terms:
        filters.append(KBChunk.chunk_text.ilike(f"%{term}%"))

    chunks = (
        db.query(KBChunk)
        .filter(or_(*filters))
        .limit(limit * 5)
        .all()
    )

    scored_chunks = []
    for chunk in chunks:
        score = simple_text_score(normalized_text, chunk.chunk_text)

        scored_chunks.append({
            "chunk": chunk,
            "score": score,
        })

    scored_chunks.sort(key=lambda x: x["score"], reverse=True)
    return scored_chunks[:limit]


def get_attachment_by_id(db: Session, attachment_id: int | None) -> Attachment | None:
    if not attachment_id:
        return None

    return db.query(Attachment).filter(Attachment.id == attachment_id).first()


def get_best_retrieval_result(db: Session, normalized_text: str) -> dict:
    """
    Combined KB + chunk retrieval result.
    """
    kb_results = search_kb_by_question(db, normalized_text, limit=3)
    chunk_results = search_chunks(db, normalized_text, limit=5)

    best_kb = kb_results[0] if kb_results else None
    best_chunk = chunk_results[0] if chunk_results else None

    selected_attachment = None

    if best_chunk and best_chunk["chunk"].attachment_id:
        selected_attachment = get_attachment_by_id(db, best_chunk["chunk"].attachment_id)
    elif best_kb and best_kb["kb"].attachments:
        selected_attachment = best_kb["kb"].attachments[0]

    return {
        "kb_results": kb_results,
        "chunk_results": chunk_results,
        "best_kb": best_kb,
        "best_chunk": best_chunk,
        "selected_attachment": selected_attachment,
    }