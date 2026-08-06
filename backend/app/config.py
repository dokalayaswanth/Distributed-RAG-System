from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "development"
    api_host: str = "127.0.0.1"
    api_port: int = 8000

    supabase_url: str = ""
    supabase_service_role_key: str = ""

    llm_api_key : str = ""
    llm_model : str = ""

    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"

    faiss_index_path: str = "data/faiss_index/index.faiss"
    faiss_metadata_path: str = "data/faiss_index/faiss_metadata.json"
    upload_dir: str = "data/uploads"
    worker_logs: str = "logs/worker_logs.txt"

    top_k_default: int = 4

    allowed_extensions: set[str] = {".pdf", ".txt"}
    allowed_content_types: set[str] = {
        "application/pdf",
        "text/plain",
    }

    max_upload_size_bytes: int = 10 * 1024 * 1024
    chunk_size:int = 1000
    chunk_overlap: int = 200

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()