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

    response = client.complete(
        messages=[
            SystemMessage(context or ""),
            UserMessage(query),
        ],
        temperature=1,
        top_p=1,
        model=model
    )

    return response.choices[0].message.content