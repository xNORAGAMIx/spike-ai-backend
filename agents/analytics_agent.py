import json
import re
from llm.client import ask_llm
from services.ga4_service import run_ga4_report

def parse_llm_json(text: str) -> dict:
    if not text or not text.strip():
        raise ValueError("LLM returned empty response")

    # Remove markdown code blocks if present
    text = re.sub(r"```json|```", "", text).strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON from LLM: {text}")

def build_ga4_plan(query: str) -> dict:
    system_prompt = """
You are a Google Analytics 4 (GA4) query planner.

You MUST return ONLY valid JSON.
NO explanations.
NO markdown.
NO backticks.
NO comments.

JSON schema:
{
  "metrics": ["string"],
  "dimensions": ["string"],
  "date_range": {
    "start": "string",
    "end": "string"
  }
}

If unsure, still return valid JSON using best guess.
"""

    response = ask_llm(system_prompt, query)
    return parse_llm_json(response)

def explain_ga4_results(query: str, rows: list, plan: dict):
    if not rows:
        return "The selected GA4 property has little or no data for this period, so no meaningful trends can be observed."

    metric = plan["metrics"][0]
    trend = analyze_trends(rows, metric)

    prompt = f"""
You are a data analyst.

User question:
{query}

Key finding:
{trend}

Explain this insight clearly and concisely in plain English.
"""

    return ask_llm(
        system_prompt="You explain GA4 results to non-technical users.",
        user_prompt=prompt
    )

def analytics_agent(query: str, property_id: str):
    try:
        plan = build_ga4_plan(query)
    except Exception as e:
        return {
            "status": "error",
            "stage": "planning",
            "message": str(e)
        }

    try:
        ga4_response = run_ga4_report(property_id, plan)
        rows = format_ga4_response(ga4_response)
    except Exception as e:
        return {
            "status": "error",
            "stage": "execution",
            "message": str(e)
        }
    
    explanation = explain_ga4_results(query, rows, plan)

    return {
        "status": "ok",
        "plan": plan,
        "rows": format_ga4_response(ga4_response),
        "explanation": explanation
    }

def analyze_trends(rows: list, metric: str):
    if len(rows) < 2:
        return "Not enough data to identify a trend."

    first = float(rows[0].get(metric, 0))
    last = float(rows[-1].get(metric, 0))

    if last > first:
        return f"{metric} shows an increasing trend over the selected period."
    elif last < first:
        return f"{metric} shows a decreasing trend over the selected period."
    else:
        return f"{metric} remains relatively stable over the selected period."

def format_ga4_response(response):
    if not response.rows:
        return []

    rows = []
    for row in response.rows:
        row_data = {}
        for i, dim in enumerate(response.dimension_headers):
            row_data[dim.name] = row.dimension_values[i].value
        for i, met in enumerate(response.metric_headers):
            row_data[met.name] = row.metric_values[i].value
        rows.append(row_data)

    return rows

# done