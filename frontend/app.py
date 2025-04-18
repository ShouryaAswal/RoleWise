import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load .env for local development
load_dotenv()

# Use secrets if on Streamlit Cloud, else fallback to local .env
API_URL = st.secrets["API_URL"] if "API_URL" in st.secrets else os.getenv("API_URL")

st.title("🔍 SHL Assessment Recommender")

# --- Health Check Section ---
if st.button("🔄 Check Backend Health"):
    try:
        res = requests.get(f"{API_URL}/health")
        if res.status_code == 200:
            st.success("✅ Backend is live and healthy!")
        else:
            st.warning(f"⚠️ Backend returned status code: {res.status_code}")
    except Exception as e:
        st.error(f"❌ Could not connect to backend: {e}")

# --- Query Section ---
st.markdown("### Enter Job Description or Natural Language Query")
query = st.text_area("")

if st.button("📥 Get Recommendations"):
    if not query.strip():
        st.warning("Please enter a job description or query.")
    else:
        try:
            res = requests.post(f"{API_URL}/recommend", json={"query": query})
            if res.status_code == 200:
                data = res.json()
                if not data["recommendations"]:
                    st.info("No recommendations found.")
                else:
                    st.markdown("### ✅ Top Recommendations")
                    for assess in data["recommendations"]:
                        st.markdown(
                            f"- **[{assess['name']}]({assess['url']})** "
                            f"({assess['duration']} mins, {assess['test_type']}) "
                            f"– Remote: {'Yes' if assess['remote_support'] else 'No'}, "
                            f"Adaptive: {'Yes' if assess['adaptive_support'] else 'No'}"
                        )
            else:
                st.error(f"API returned an error: {res.status_code}")
        except Exception as e:
            st.error(f"❌ Request failed: {e}")
