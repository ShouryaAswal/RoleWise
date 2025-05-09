import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv

load_dotenv()

def generate_answer(query, context):
    endpoint = "https://models.github.ai/inference"
    model = "openai/gpt-4.1"
    token = os.environ["GITHUB_TOKEN"]

    client = ChatCompletionsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(token),
    )

    system_prompt = (
        "You are an expert on SHL assessments. "
        "Given the following assessment information, answer the user's query extremely concisely. "
        "Your answer contains one thing only - A small description of how the answer provided by the context is relavent to the query. No more no less. "
        "Answer should be 2-4 lines of information only "
    )

    response = client.complete(
        messages=[
            SystemMessage(system_prompt + "\n\n" + (context or "")),
            UserMessage(query),
        ],
        temperature=1,
        top_p=1,
        model=model
    )

    return response.choices[0].message.content