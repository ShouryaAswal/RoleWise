from agentic_model import agentic_process

def run_tests():
    queries = [
        "hi, I wanted to know what is SHL?",
        "Can you help to get an assessment for java developers",
        "Tell me about the weather today."
    ]
    for q in queries:
        result = agentic_process(q)
        print(f"Query: {q}")
        for ans in result["answers"]:
            print(f"Title: {ans['title']}")
            print(f"URL: {ans['url']}")
            print(f"Answer: {ans['llm_answer']}\n")

if __name__ == "__main__":
    run_tests()
