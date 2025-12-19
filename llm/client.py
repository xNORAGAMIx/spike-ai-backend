from openai import OpenAI
import os
from dotenv import load_dotenv # type: ignore

load_dotenv()

client = OpenAI(
    api_key=os.getenv("sk-mAGfqCb_a82u-w8-lSkFvg"),
    base_url="http://3.110.18.218/"
)

def classify_intent(query: str) -> str:
    prompt = f"""
You are an intent classifier.

Classify the following query into one of:
- analytics
- seo
- analytics_seo

Rules:
- If the query mentions traffic, views, users, sessions, GA4, analytics → analytics
- If the query mentions title tags, meta description, indexability, HTTPS, SEO → seo
- If both analytics and SEO concepts are mentioned → analytics_seo

Return ONLY the intent string.

Query:
{query}
"""

    response = client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return response.choices[0].message.content.strip() # type: ignore

def ask_llm(system_prompt: str, user_prompt: str) -> str:
    response = client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0
    )
    return response.choices[0].message.content.strip() # type: ignore

