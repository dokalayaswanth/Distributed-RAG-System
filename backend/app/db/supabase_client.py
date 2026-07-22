from functools import lru_cache

from supabase import Client, create_client

from app.config import settings


@lru_cache
def get_supabase_client() -> Client:
    if not settings.supabase_url:
        raise ValueError("SUPABASE_URL is missing from environment variables.")

    if not settings.supabase_service_role_key:
        raise ValueError("SUPABASE_SERVICE_ROLE_KEY is missing from environment variables.")
    return create_client(
        settings.supabase_url,
        settings.supabase_service_role_key,
    )