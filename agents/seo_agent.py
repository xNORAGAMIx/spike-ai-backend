from services.sheets_service import load_seo_dataframe
from llm.client import ask_llm
import json
import re
import math

def build_seo_plan(query: str, columns: list):
    system_prompt = f"""
You are an SEO analyst.

Available columns:
{columns}

Convert the user query into a STRICT JSON plan.

JSON schema:
{{
  "filters": [
    {{
      "column": "string",
      "operator": "equals | not_equals | contains | gt | lt",
      "value": "string or number"
    }}
  ],
  "group_by": ["string"] | null,
  "aggregation": {{
    "type": "count | percentage",
    "column": "string"
  }} | null
}}

Rules:
- Use only available columns
- No explanations
- No markdown
"""

    response = ask_llm(system_prompt, query)
    response = re.sub(r"```json|```", "", response).strip()
    return json.loads(response)

def apply_seo_plan(df, plan):
    filtered = df.copy()

    for f in plan.get("filters", []):
        col = f["column"]
        op = f["operator"]
        val = f["value"]

        if col not in filtered.columns:
            continue

        if op == "equals":
            filtered = filtered[filtered[col] == val]
        elif op == "not_equals":
            filtered = filtered[filtered[col] != val]
        elif op == "contains":
            filtered = filtered[filtered[col].astype(str).str.contains(val, na=False)]
        elif op == "gt":
            filtered = filtered[filtered[col].astype(float) > float(val)]
        elif op == "lt":
            filtered = filtered[filtered[col].astype(float) < float(val)]

    # Grouping
    if plan.get("group_by"):
        group_col = plan["group_by"][0]
        grouped = filtered.groupby(group_col).size().reset_index(name="count")
        return grouped.to_dict(orient="records")

    # Aggregation
    if plan.get("aggregation"):
        agg = plan["aggregation"]
        if agg["type"] == "count":
            return { "count": len(filtered) }

        if agg["type"] == "percentage":
            total = len(df)

            if total == 0 or len(filtered) == 0:
                return {
                    "percentage": 0.0,
                    "note": "No matching rows found for the given condition"
                }
            return {
                "percentage": round((len(filtered) / total) * 100, 2)
            }

    return filtered.head(50).to_dict(orient="records")

def clean_nan(obj):
    if isinstance(obj, float) and math.isnan(obj):
        return None
    if isinstance(obj, dict):
        return {k: clean_nan(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [clean_nan(v) for v in obj]
    return obj

def seo_agent(query: str):
    df = load_seo_dataframe()

    plan = build_seo_plan(query, df.columns.tolist())
    result = apply_seo_plan(df, plan)

    return {
    "status": "ok",
    "plan": plan,
    "result": clean_nan(result)
}

# done