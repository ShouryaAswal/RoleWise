import os
from openai import OpenAI

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

def call_openai(prompt, context=None, model="gpt-3.5-turbo"):
    messages = []
    if context:
        messages.append({"role": "system", "content": context})
    messages.append({"role": "user", "content": prompt})
    resp = client.chat.completions.create(
        model=model,
        messages=messages
    )
    return resp.choices[0].message.content

# Add Gemini support here if needed
