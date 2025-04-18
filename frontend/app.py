import streamlit as st
import requests
import os
from dotenv import load_dotenv

API_URL = os.getenv("URL")

st.title("SHL Assessment Recommender")
query = st.text_area("Enter Job Description or Query")

if st.button("Get Recommendations"):
    res = requests.post(f"{API_URL}/recommend", json={"query": query})
    data = res.json()
    for assess in data["recommendations"]:
        st.write(f"**[{assess['name']}]({assess['url']})** - {assess['duration']} mins")
