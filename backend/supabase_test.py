# supabase_test.py
from supabase import create_client
import os
from dotenv import load_dotenv

# Load .env for local development
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def test_connection():
    try:
        print(" Connected to Supabase")

        # Insert test
        insert_res = supabase.table("assessments").insert({
            "assessment_name": "Test Title",
            "remote_testing": True,
            "adaptive_irt" : True
        }).execute()
        print(" Insert result:", insert_res)

        # Read test
        select_res = supabase.table("assessments").select("*").limit(1).execute()
        print(" Fetch result:", select_res)

        # Delete test
        if select_res.data:
            test_id = select_res.data[0]["id"]
            delete_res = supabase.table("assessments").delete().eq("id", test_id).execute()
            print(" Delete result:", delete_res)

    except Exception as e:
        print(" Error connecting to Supabase:", e)

if __name__ == "__main__":
    test_connection()
