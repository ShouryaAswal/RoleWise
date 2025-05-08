import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load .env for local development
load_dotenv()

# Unified backend URL (used for both health and recommend)
BACKEND_URL = st.secrets["BACKEND_URL"] if "BACKEND_URL" in st.secrets else os.getenv("BACKEND_URL")

st.title("🔍 SHL Assessment Recommender")


st.title("Assessment Chatbot")
query = st.text_input("Ask about assessments:")

if st.button("Submit") and query:
    response = requests.post("http://localhost:8000/query", json={"query": query})
    data = response.json()
    st.write("**Answer:**", data["answer"])
    st.write("**Top 3 Assessments:**")
    for meta in data["top_assessments"]:
        st.write(meta)
