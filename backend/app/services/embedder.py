from functools import lru_cache
from sentence_transformers import SentenceTransformer
from app.config import settings

@lru_cache
def get_embeddings_model() -> SentenceTransformer:
    return SentenceTransformer(settings.embedding_model)

def embed_text(text: str) -> list[float]:
    if not text or not text.strip():
        raise ValueError("Text cannot be empty.")
    model = get_embeddings_model()
    embeddings = model.encode(text.strip())
    return embeddings.tolist()
    
def embed_texts(texts: list[str]) -> list[list[float]]:
    if not texts:
        raise ValueError("Texts cannot be empty.")
    cleaned_texts = []
    for text in texts:
        if not text or not text.strip():
            raise ValueError("Text list cannot contain empty text")
        cleaned_texts.append(text.strip())
    model = get_embeddings_model()
    embeddings = model.encode(cleaned_texts)
    return embeddings.tolist()