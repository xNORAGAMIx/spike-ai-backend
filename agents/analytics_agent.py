from llm.client import ask_llm

def build_ga4_plan(query: str) -> dict:
    system_prompt = """
You are a Google Analytics 4 (GA4) expert.

Your task:
Convert a natural-language analytics question into a GA4 reporting plan.

Return STRICT JSON with:
- metrics (array of GA4 metric names)
- dimensions (array of GA4 dimension names)
- date_range { start, end }
- filters (optional)
- order_by (optional)

Rules:
- Use valid GA4 metrics and dimensions
- Use relative dates like "7daysAgo", "30daysAgo", "today"
- Do NOT include explanations
- Do NOT include markdown
"""

    response = ask_llm(system_prompt, query)

    return response # type: ignore
