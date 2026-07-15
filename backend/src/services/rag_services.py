from typing import List, Dict
from sqlalchemy.orm import Session
from sqlalchemy import text
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from src.config.env import settings
from src.utils.text_normalizer import normalize_for_search

# Lazy singletons
_embed_model = None
_llm_pipe = None


def get_embed_model():
    global _embed_model
    if _embed_model is None:
        _embed_model = SentenceTransformer(settings.HF_EMBED_MODEL)
    return _embed_model


def get_llm_pipe():
    global _llm_pipe
    if _llm_pipe is None:
        tokenizer = AutoTokenizer.from_pretrained(settings.HF_LLM_MODEL)
        model = AutoModelForCausalLM.from_pretrained(
            settings.HF_LLM_MODEL,
            device_map="auto"
        )
        _llm_pipe = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            max_new_tokens=settings.MAX_NEW_TOKENS,
            do_sample=True,
            temperature=0.2
        )
    return _llm_pipe


def embed_text(text_value: str) -> List[float]:
    model = get_embed_model()
    vector = model.encode(text_value, normalize_embeddings=True)
    return vector.tolist()


def retrieve_relevant_chunks(db: Session, user_query: str, top_k: int = 4) -> List[Dict]:
    normalized = normalize_for_search(user_query)
    query_embedding = embed_text(normalized)

    sql = text("""
        SELECT
            c.chunk_id,
            c.chunk_text,
            kb.kb_id,
            kb.title,
            kb.department_key,
            1 - (c.embedding <=> CAST(:embedding AS vector)) AS score
        FROM software_engineering.kb_chunks c
        JOIN software_engineering.knowledge_base kb
            ON kb.kb_id = c.kb_id
        ORDER BY c.embedding <=> CAST(:embedding AS vector)
        LIMIT :top_k
    """)

    rows = db.execute(
        sql,
        {
            "embedding": str(query_embedding),
            "top_k": top_k
        }
    ).mappings().all()

    return [dict(row) for row in rows]


def build_context(chunks: List[Dict]) -> str:
    if not chunks:
        return "No relevant database context found."

    parts = []
    for i, chunk in enumerate(chunks, start=1):
        parts.append(
            f"[Source {i}] Title: {chunk['title']}\n"
            f"Content: {chunk['chunk_text']}\n"
            f"Relevance: {round(float(chunk['score']), 4)}"
        )
    return "\n\n".join(parts)


def generate_answer_from_context(user_query: str, context: str) -> str:
    llm = get_llm_pipe()

    prompt = f"""
You are QueryMate AI for Software Engineering department.

Rules:
- Answer only from the provided context.
- If the answer is not in context, say clearly:
  "I could not find this in the department knowledge base."
- Keep answer helpful, direct, and student-friendly.
- If policy/course/outline is mentioned, summarize clearly.

Context:
{context}

Question:
{user_query}

Answer:
""".strip()

    result = llm(prompt)[0]["generated_text"]

    if "Answer:" in result:
        return result.split("Answer:", 1)[-1].strip()

    return result.strip()


def answer_query_with_rag(db: Session, user_query: str) -> tuple[str, List[Dict]]:
    chunks = retrieve_relevant_chunks(db, user_query, settings.TOP_K)
    context = build_context(chunks)
    answer = generate_answer_from_context(user_query, context)
    return answer, chunks