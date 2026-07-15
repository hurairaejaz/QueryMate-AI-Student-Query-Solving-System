from sentence_transformers import SentenceTransformer, util
from src.models.kb_content import KnowledgeBase

_embed_model = None


def get_embed_model():
    global _embed_model
    if _embed_model is None:
        # Better multilingual matching
        _embed_model = SentenceTransformer("BAAI/bge-m3")
    return _embed_model


def semantic_search_kb(
    db,
    query_text: str,
    department_key: str = "software_engineering",
    top_k: int = 5,
):
    rows = (
        db.query(KnowledgeBase)
        .filter(KnowledgeBase.department_key == department_key)
        .all()
    )

    if not rows:
        return []

    corpus = []
    for row in rows:
        title = row.title or ""
        content = row.content or ""
        corpus.append(f"{title}. {content}")

    model = get_embed_model()

    query_emb = model.encode(
        query_text,
        convert_to_tensor=True,
        normalize_embeddings=True,
    )
    doc_embs = model.encode(
        corpus,
        convert_to_tensor=True,
        normalize_embeddings=True,
    )

    scores = util.cos_sim(query_emb, doc_embs)[0]

    results = []
    for idx, row in enumerate(rows):
        results.append({
            "kb": row,
            "semantic_score": float(scores[idx]),
        })

    results.sort(key=lambda x: x["semantic_score"], reverse=True)
    return results[:top_k]