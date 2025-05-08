import streamlit as st
import requests
import os
from dotenv import load_dotenv


load_dotenv()
BACKEND_URL = os.getenv("BACKEND_URL")

st.title("🔍 SHL Assessment Recommender")


st.title("Assessment Chatbot")
query = st.text_input("Ask about assessments:")

if st.button("Submit") and query:
    with st.spinner("Getting answer..."):
        response = requests.post(f"{BACKEND_URL}/query", json={"query": query})
        st.write(f"Request sent to: {BACKEND_URL}/query")
        if response.status_code == 200:
            try:
                data = response.json()
            except Exception as e:
                st.error(f"Error decoding JSON: {e}")
                st.write("Raw response:", response.text)
                data = {"answers": []}
        else:
            st.error(f"Backend error: {response.status_code}")
            st.write("Raw response:", response.text)
            data = {"answers": []}
    st.write("**Answers:**")
    for ans in data["answers"]:
        st.markdown(f"**[{ans['title']}]({ans['url']})**")
        st.write(ans["llm_answer"])
        st.markdown("---")
