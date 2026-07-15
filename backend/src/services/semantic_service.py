from typing import List, Dict, Tuple
from sqlalchemy.orm import Session
from sentence_transformers import SentenceTransformer, util

from src.models.kb_content import KnowledgeBase

_embed_model = None

def get_embed_model():
    global _embed_model
    if _embed_model is None:
        # multilingual  use case
        _embed_model = SentenceTransformer("BAAI/bge-m3")
    return _embed_model


def get_all_kb_rows(db: Session, department_key: str = "software_engineering"):
    return (
        db.query(KnowledgeBase)
        .filter(KnowledgeBase.department_key == department_key)
        .all()
    )


def semantic_search_kb(
    db: Session,
    query_text: str,
    department_key: str = "software_engineering",
    top_k: int = 5
) -> List[Dict]:
    rows = get_all_kb_rows(db, department_key)

    if not rows:
        return []

    corpus = []
    for row in rows:
        title = row.title or ""
        content = row.content or ""
        corpus.append(f"{title}. {content}")

    model = get_embed_model()

    query_emb = model.encode(query_text, convert_to_tensor=True, normalize_embeddings=True)
    doc_embs = model.encode(corpus, convert_to_tensor=True, normalize_embeddings=True)

    scores = util.cos_sim(query_emb, doc_embs)[0]

    results = []
    for idx, row in enumerate(rows):
        results.append({
            "kb": row,
            "semantic_score": float(scores[idx]),
        })

    results.sort(key=lambda x: x["semantic_score"], reverse=True)
    return results[:top_k]