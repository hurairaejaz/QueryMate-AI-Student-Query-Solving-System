from sqlalchemy.orm import Session
from src.models.kb_content import KnowledgeBase
from src.models.kb_chunks import KBChunk
from src.services.rag_services import embed_text


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 100):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks


def ingest_kb_record(db: Session, kb: KnowledgeBase):
    # Remove old chunks if re-ingesting
    db.query(KBChunk).filter(KBChunk.kb_id == kb.kb_id).delete()

    full_text = f"{kb.title}\n\n{kb.content}"
    chunks = chunk_text(full_text)

    for idx, chunk in enumerate(chunks):
        vector = embed_text(chunk)
        db_chunk = KBChunk(
            kb_id=kb.kb_id,
            chunk_index=idx,
            chunk_text=chunk,
            embedding=vector
        )
        db.add(db_chunk)

    db.commit()