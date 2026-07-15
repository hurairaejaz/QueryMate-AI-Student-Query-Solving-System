from sqlalchemy.orm import Session

from src.models.kb_chunks import KBChunk
from src.utils.chunking import split_text_into_chunks


def delete_old_chunks_for_attachment(db: Session, attachment_id: int) -> None:
    db.query(KBChunk).filter(KBChunk.attachment_id == attachment_id).delete()
    db.commit()


def create_chunks_for_attachment(
    db: Session,
    kb_id: int,
    attachment_id: int | None,
    extracted_text: str,
    chunk_size: int = 500,
    overlap: int = 50,
) -> list[KBChunk]:
    if not extracted_text or not extracted_text.strip():
        return []

    chunks = split_text_into_chunks(
        text=extracted_text,
        chunk_size=chunk_size,
        overlap=overlap,
    )

    created_chunks = []

    for index, chunk_text in enumerate(chunks):
        chunk = KBChunk(
            kb_id=kb_id,
            attachment_id=attachment_id,
            chunk_index=index,
            chunk_text=chunk_text,
        )
        db.add(chunk)
        created_chunks.append(chunk)

    db.commit()

    for chunk in created_chunks:
        db.refresh(chunk)

    return created_chunks


def rebuild_chunks_for_attachment(
    db: Session,
    kb_id: int,
    attachment_id: int | None,
    extracted_text: str,
    chunk_size: int = 500,
    overlap: int = 50,
) -> list[KBChunk]:
    if attachment_id:
        delete_old_chunks_for_attachment(db, attachment_id)

    return create_chunks_for_attachment(
        db=db,
        kb_id=kb_id,
        attachment_id=attachment_id,
        extracted_text=extracted_text,
        chunk_size=chunk_size,
        overlap=overlap,
    )