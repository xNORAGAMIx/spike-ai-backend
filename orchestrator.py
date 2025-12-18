from llm.client import classify_intent
from agents.analytics_agent import build_ga4_plan

def handle_query(query: str, property_id: str | None):
    intent = classify_intent(query)

    if intent == "analytics":
        plan = build_ga4_plan(query)
        return {
            "status": "ok",
            "intent": intent,
            "ga4_plan": plan,
            "message": "Step 3: GA4 query plan generated"
        }

    return {
        "status": "ok",
        "intent": intent,
        "message": "Non-analytics intent (not handled yet)"
    }
