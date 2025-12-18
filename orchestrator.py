from llm.client import classify_intent
from agents.analytics_agent import analytics_agent
from agents.seo_agent import seo_agent 

def handle_query(query: str, property_id: str | None):
    intent = classify_intent(query)

    if intent == "seo":
        return seo_agent(query)

    if intent == "analytics":
        if not property_id:
            return {
                "status": "error",
                "message": "propertyId is required for analytics queries"
            }

        return analytics_agent(query, property_id)

    return {
        "status": "ok",
        "intent": intent,
        "message": "Intent detected, agent not implemented yet"
    }
