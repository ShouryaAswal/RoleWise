from langchain_google_genai import ChatGoogleGenerativeAI
from rag_agent import process_query
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize Gemini LLM with API Key from environment
gemini_api_key = os.getenv("GEMINI_API_KEY")

if gemini_api_key is None:
    raise ValueError("Gemini API key is not set in the environment variables.")

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0, api_key=gemini_api_key)

# Classifier function using Gemini
def classify_query_with_gemini(query):
    prompt = (
        "You are a query classifier. Classify the user's intent into one of the following categories:\n"
        "- shl_info: if the query is asking what SHL is or about SHL in general\n"
        "- assessment_query: if the query is seeking information about an SHL assessment or test\n"
        "- irrelevant: if the query is unrelated to SHL or assessments\n\n"
        f"Query: {query}\n"
        "Category:"
    )
    try:
        response = llm.invoke(prompt)
        return response.content.strip().lower()
    except Exception:
        return "irrelevant"

# Main agent function
def agentic_process(query):
    category = classify_query_with_gemini(query)

    if category == "shl_info":
        return {
            "answers": [
                {
                    "title": "SHL Overview",
                    "url": "https://www.shl.com/",
                    "llm_answer": "SHL is a global leader in talent innovation, providing assessment and talent solutions for organizations."
                }
            ]
        }
    elif category == "assessment_query":
        return process_query(query)
    else:
        return {
            "answers": [
                {
                    "title": "No Match",
                    "url": "#",
                    "llm_answer": "Your query could not be matched to an SHL topic or assessment category."
                }
            ]
        }

# Optional for local testing
if __name__ == "__main__":
    test_query = input("Enter a query: ")
    result = agentic_process(test_query)
    print(result)
