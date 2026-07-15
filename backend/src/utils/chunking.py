from typing import List


def split_text_into_chunks(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """
    Split long text into overlapping chunks for retrieval.

    Args:
        text: Full document text
        chunk_size: Maximum chunk length
        overlap: Overlap between consecutive chunks

    Returns:
        List of text chunks
    """
    if not text:
        return []

    text = " ".join(text.split())
    if len(text) <= chunk_size:
        return [text]

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = min(start + chunk_size, text_length)
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= text_length:
            break

        start = max(end - overlap, 0)

    return chunks