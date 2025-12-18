from llm.client import classify_intent

def handle_query(query: str, property_id: str | None):
    intent = classify_intent(query)

    return {
        "status": "ok",
        "intent": intent,
        "query": query,
        "property_id": property_id,
        "message": "Step 2: intent detected"
    }
