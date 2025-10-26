# supabase_client.py
import os
from supabase import create_client, Client

# Fetch from environment variables (like your RN code)
SUPABASE_URL = os.getenv("EXPO_PUBLIC_SUPABASE_URL", "")
SUPABASE_ANON_KEY = os.getenv("EXPO_PUBLIC_SUPABASE_ANON_KEY", "")

# Create Supabase client
supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_ANON_KEY,
    # supabase-py handles auth differently; no autoRefreshToken or detectSessionInUrl
    # Sessions persist automatically in the client object
)

# Example usage
if __name__ == "__main__":
    try:
        response = supabase.table("user_preferences").select("*").execute()
        print("Connected to Supabase successfully:", response.data)
    except Exception as e:
        print("Supabase connection error:", e)
