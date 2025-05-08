from rag_agent import process_query

def agentic_process(query):
    q_lower = query.lower()
    if "what is shl" in q_lower:
        return {
            "answers": [
                {
                    "title": "SHL Overview",
                    "url": "https://www.shl.com/",
                    "llm_answer": "SHL is a global leader in talent innovation, providing assessment and talent solutions for organizations."
                }
            ]
        }
    elif "assessment" in q_lower:
        return process_query(query)
    else:
        return {
            "answers": [
                {
                    "title": "No Match",
                    "url": "#",
                    "llm_answer": "Your query could not be processed by the agentic model."
                }
            ]
        }