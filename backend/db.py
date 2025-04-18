from supabase import create_client
import os

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

supabase = create_client(url, key)

def fetch_assessments():
    return supabase.table("assessments").select("*").execute().data
