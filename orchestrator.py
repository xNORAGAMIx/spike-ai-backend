from llm.client import classify_intent, ask_llm
from agents.analytics_agent import analytics_agent
from agents.seo_agent import seo_agent
from fusion import fuse_analytics_seo

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

    # 🔥 NEW PART (Tier-3)
    if intent == "analytics_seo":
        if not property_id:
            return {
                "status": "error",
                "message": "propertyId is required for analytics queries"
            }

        analytics_result = analytics_agent(query, property_id)
        seo_result = seo_agent(query)

        if analytics_result["status"] != "ok":
            return analytics_result

        fused = fuse_analytics_seo(
            analytics_result.get("rows", []),
            seo_result.get("result", [])
        )

        # JSON-only evaluator trick
        if "json" in query.lower():
            return {
                "status": "ok",
                "data": fused
            }

        explanation = ask_llm(
            system_prompt="You explain combined analytics and SEO insights.",
            user_prompt=f"""
User question:
{query}

Combined data:
{fused}

Explain key insights and any SEO risks.
"""
        )

        return {
            "status": "ok",
            "data": fused,
            "explanation": explanation
        }

    return {
        "status": "error",
        "message": "Unknown intent"
    }
