import json
from pathlib import Path

import faiss
import numpy as np

from app.config import settings


def create_index(dimension: int):
    if dimension <= 0:
        raise ValueError("Vector dimension must be greater than 0.")

    return faiss.IndexFlatIP(dimension)


def save_index(index, path: str | None = None) -> None:
    index_path = Path(path or settings.faiss_index_path)

    index_path.parent.mkdir(parents=True, exist_ok=True)

    faiss.write_index(index, str(index_path))


def load_index(path: str | None = None):
    index_path = Path(path or settings.faiss_index_path)

    if not index_path.exists():
        raise FileNotFoundError(f"FAISS index file does not exist: {index_path}")

    return faiss.read_index(str(index_path))


def save_metadata(metadata: dict[str, dict], path: str | None = None) -> None:
    metadata_path = Path(path or settings.faiss_metadata_path)

    metadata_path.parent.mkdir(parents=True, exist_ok=True)

    with open(metadata_path, "w", encoding="utf-8") as file:
        json.dump(metadata, file, indent=2, ensure_ascii=False)


def load_metadata(path: str | None = None) -> dict[str, dict]:
    metadata_path = Path(path or settings.faiss_metadata_path)

    if not metadata_path.exists():
        return {}

    with open(metadata_path, "r", encoding="utf-8") as file:
        return json.load(file)


def _to_float32_array(vectors: list[list[float]]) -> np.ndarray:
    if not vectors:
        raise ValueError("Vector list cannot be empty.")

    dimension = len(vectors[0])

    if dimension == 0:
        raise ValueError("Vectors cannot be empty.")

    for vector in vectors:
        if len(vector) != dimension:
            raise ValueError("All vectors must have the same dimension.")

    return np.array(vectors, dtype="float32")


def add_vectors(vectors: list[list[float]], metadata: list[dict]) -> dict:
    if not metadata:
        raise ValueError("Metadata list cannot be empty.")

    if len(vectors) != len(metadata):
        raise ValueError("Vectors and metadata must have the same length.")

    vector_array = _to_float32_array(vectors)

    faiss.normalize_L2(vector_array)

    dimension = vector_array.shape[1]

    try:
        index = load_index()
        existing_metadata = load_metadata()

        if index.d != dimension:
            raise ValueError(
                f"Existing index dimension {index.d} does not match vector dimension {dimension}."
            )

    except FileNotFoundError:
        index = create_index(dimension)
        existing_metadata = {}

    start_position = index.ntotal
    vector_positions = []

    index.add(vector_array)

    for offset, item in enumerate(metadata):
        vector_index = start_position + offset
        vector_positions.append(vector_index)

        metadata_item = item.copy()
        metadata_item["vector_index"] = vector_index

        existing_metadata[str(vector_index)] = metadata_item

    save_index(index)
    save_metadata(existing_metadata)

    return {
        "added_count": len(vectors),
        "total_vectors": index.ntotal,
        "metadata_count": len(existing_metadata),
        "vector_positions": vector_positions
    }


def search_vectors(query_vector: list[float], top_k: int = 5) -> list[dict]:
    if not query_vector:
        raise ValueError("Query vector cannot be empty.")

    if top_k <= 0:
        raise ValueError("top_k must be greater than 0.")

    index = load_index()
    metadata = load_metadata()

    query_array = np.array([query_vector], dtype="float32")

    if query_array.shape[1] != index.d:
        raise ValueError(
            f"Query vector dimension {query_array.shape[1]} does not match index dimension {index.d}."
        )

    faiss.normalize_L2(query_array)

    search_k = min(top_k, index.ntotal)

    scores, positions = index.search(query_array, search_k)

    results = []

    for score, position in zip(scores[0], positions[0]):
        if position == -1:
            continue

        vector_index = int(position)
        metadata_item = metadata.get(str(vector_index))

        results.append(
            {
                "score": float(score),
                "vector_index": vector_index,
                "metadata": metadata_item,
            }
        )

    return results