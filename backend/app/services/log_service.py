from app.db.supabase_client import get_supabase_client
def query_log(log: dict):
    if not log:
        raise ValueError("Log data should not be empty.")
    supabase = get_supabase_client()
    response = supabase.table("query_logs").insert(log).execute()

    if not response.data:
        raise Exception(f"Failed to retrieve query logs: {response.status_code} - {response.text}")

    return response.data[0]