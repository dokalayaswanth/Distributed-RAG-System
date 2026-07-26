from app.config import settings

def chunk_text(text: str, chunk_size: int | None = None, chunk_overlap: int | None = None)->list[dict]:
    chunk_size = chunk_size if chunk_size is not None else settings.chunk_size
    chunk_overlap = chunk_overlap if chunk_overlap is not None else settings.chunk_overlap

    if chunk_size <= 0:
        raise ValueError("Chunk size must be greater than 0.")

    if chunk_overlap < 0:
        raise ValueError("Chunk overlap cannot be negative.")

    if chunk_overlap >= chunk_size:
        raise ValueError("Chunk overlap must be smaller than chunk size.")
    
    cleaned_text = text.strip()

    if not cleaned_text:
        raise ValueError("Text cannot be empty.")

    chunks: list[dict] = []
    start = 0
    chunk_index =0
    text_length = len(cleaned_text)

    while start < text_length:
        end = min(start + chunk_size, text_length)

        chunk_content = cleaned_text[start: end]

        chunks.append({
            "chunk_index": chunk_index,
            "content": chunk_content
        })

        if end == text_length:
            break

        chunk_index+=1
        start = end - chunk_overlap
    
    return chunks