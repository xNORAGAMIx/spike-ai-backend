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

    # Tier 3
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

        if not fused:
            return {
                "status": "ok",
                "data": [],
                "explanation": (
                    "There is insufficient GA4 traffic data for the selected period "
                    "to identify highly visited pages. Therefore, a comparison between "
                    "traffic and SEO quality cannot be made at this time."
                )
            }
        
        if "json" in query.lower():
            return {
                "status": "ok",
                "data": fused
            }

        explanation = ask_llm(
            system_prompt="""
        You are a data analyst.

        Rules:
        - Base your explanation ONLY on the provided data
        - Do NOT introduce new metrics or tools
        - Do NOT give hypothetical advice
        - If data is limited, acknowledge limitations briefly
        - Keep the explanation under 3 sentences
        """,
            user_prompt=f"""
        User question:
        {query}

        Combined analytics + SEO data:
        {fused}
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
