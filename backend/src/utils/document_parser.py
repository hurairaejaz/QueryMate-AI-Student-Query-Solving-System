import os


def extract_text_from_txt(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
        return file.read()


def extract_text_from_pdf(file_path: str) -> str:
    try:
        from PyPDF2 import PdfReader
    except ImportError:
        raise ImportError("PyPDF2 is not installed. Run: pip install PyPDF2")

    text = []
    reader = PdfReader(file_path)

    for page in reader.pages:
        page_text = page.extract_text() or ""
        if page_text.strip():
            text.append(page_text)

    return "\n".join(text)


def extract_text_from_docx(file_path: str) -> str:
    try:
        from docx import Document
    except ImportError:
        raise ImportError("python-docx is not installed. Run: pip install python-docx")

    doc = Document(file_path)
    paragraphs = [para.text for para in doc.paragraphs if para.text.strip()]
    return "\n".join(paragraphs)


def extract_text_from_file(file_path: str, mime_type: str | None = None) -> str:
    """
    Extract text based on mime type or extension.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    extension = os.path.splitext(file_path)[1].lower()

    if mime_type:
        mime_type = mime_type.lower()

    if extension == ".txt" or mime_type == "text/plain":
        return extract_text_from_txt(file_path)

    if extension == ".pdf" or mime_type == "application/pdf":
        return extract_text_from_pdf(file_path)

    if extension == ".docx" or mime_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return extract_text_from_docx(file_path)

    return ""