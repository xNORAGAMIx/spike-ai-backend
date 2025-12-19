# Spike AI Builder Hackathon – AI Analytics & SEO Backend

> **Production‑ready, agent‑based AI backend for GA4 analytics and SEO audits**

---

## Overview

This project implements a **headless, production‑grade AI backend** capable of answering **natural‑language questions** about:

* **Web Analytics (Google Analytics 4)** – live data via GA4 Data API
* **SEO Audits (Screaming Frog exports)** – live ingestion from Google Sheets

The system is designed around **agent‑based reasoning**, where each domain (Analytics, SEO) is handled by an independent agent and coordinated through a central **Orchestrator**.

There is **no frontend UI by design** — the entire system is evaluated through a single HTTP API.

---

## Key Capabilities

### Tier 1 – Analytics Agent (GA4)

* Natural‑language → GA4 reporting plan inference
* Live GA4 Data API execution
* Dynamic `propertyId` support (evaluator‑safe)
* Server‑side validation of metrics & dimensions
* Time‑series and aggregate reporting
* Graceful handling of empty or sparse GA4 properties
* Clear, human‑readable analytical explanations

### Tier 2 – SEO Agent (Screaming Frog)

* Live ingestion of SEO audit data from Google Sheets
* Schema‑safe filtering, grouping, and aggregation
* Conditional logic (e.g., HTTPS, title length, indexability)
* JSON‑only output when explicitly requested

### Tier 3 – Multi‑Agent Orchestration

* Automatic intent detection (`analytics`, `seo`, `analytics_seo`)
* Cross‑agent routing and execution
* Deterministic data fusion (Analytics + SEO)
* Unified response with optional AI‑generated insights

---

## 🧠 System Architecture

```
Client (curl / evaluator)
        ↓
POST /query
        ↓
Orchestrator
  ├─ Intent Detection (LLM)
  ├─ Agent Routing
  ├─ Multi‑Agent Coordination
        ↓
┌──────────────────────────────┐
│ Analytics Agent (GA4)         │
│  • Query Planning (LLM)       │
│  • Field Validation           │
│  • GA4 Data API (Live)        │
└──────────────────────────────┘
        ↓
┌──────────────────────────────┐
│ SEO Agent (Screaming Frog)    │
│  • Live Google Sheets Ingest  │
│  • Pandas‑based Logic         │
└──────────────────────────────┘
        ↓
Fusion Layer (Code‑Driven)
        ↓
LLM Explanation (Optional)
        ↓
JSON Response
```

### Design Principles

* **Separation of concerns** (Orchestrator ≠ Agents)
* **LLM as a reasoning tool, not a data source**
* **Deterministic execution, explainable outputs**
* **Evaluator‑safe & property‑agnostic**

---

## API (Fixed)

### Endpoint

```
POST http://localhost:8080/query
```

### Request Body

#### Analytics or Multi‑Agent Queries

```json
{
  "propertyId": "<GA4_PROPERTY_ID>",
  "query": "Natural language question"
}
```

#### SEO‑Only Queries

```json
{
  "query": "Natural language question"
}
```

### Example Queries

**GA4 Analytics**

```json
{
  "propertyId": "123456789",
  "query": "Give me a daily breakdown of page views and users for the pricing page over the last 14 days and summarize trends"
}
```

**SEO Audit**

```json
{
  "query": "Which URLs do not use HTTPS and have title tags longer than 60 characters?"
}
```

**Multi‑Agent (Analytics + SEO)**

```json
{
  "propertyId": "123456789",
  "query": "What are the top 10 pages by views and their title tags?"
}
```

---

## Tech Stack

* **Backend Framework:** FastAPI (Python)
* **AI / LLM Access:** LiteLLM Proxy (Google Gemini models)
* **Analytics API:** Google Analytics Data API (GA4)
* **SEO Processing:** Pandas + Google Sheets (CSV export)
* **Server:** Uvicorn

---

## Project Structure

```
spike-ai-backend/
├── main.py                  # FastAPI entrypoint
├── orchestrator.py          # Intent detection & agent routing
├── fusion.py                # Cross‑agent data fusion
├── agents/
│   ├── analytics_agent.py   # GA4 reasoning + execution
│   └── seo_agent.py         # SEO reasoning + data processing
├── services/
│   ├── ga4_service.py       # GA4 Data API wrapper
│   └── sheets_service.py   # Live Google Sheets ingestion
├── llm/
│   └── client.py            # LiteLLM client abstraction
├── credentials.json         # GA4 service account (replaced by evaluators)
├── deploy.sh                # One‑command deployment
├── requirements.txt
└── README.md
```

---

## Setup & Run Instructions

### Prerequisites

* Python 3.10+
* Internet access
* LiteLLM API key

### Run the Application

```bash
bash deploy.sh
```

This will:

1. Create a virtual environment (`.venv`)
2. Install all dependencies
3. Start the server on **port 8080**

Startup completes within the required time window.

---

## Credentials & Evaluation Safety

* **`credentials.json` is loaded dynamically at runtime**
* No GA4 credentials or `propertyId` values are hardcoded
* During evaluation, Spike AI can safely replace:

  * `credentials.json`
  * `propertyId` in API requests

No code changes are required for evaluation.

---

## Error Handling & Robustness

* Empty GA4 properties handled gracefully
* Invalid LLM output safely parsed and validated
* GA4 field allow‑listing prevents invalid queries
* Clear error stages (`planning`, `execution`)
* JSON‑only responses supported when explicitly requested

---

## Assumptions & Limitations

### Assumptions

* GA4 metrics/dimensions used are commonly supported
* Screaming Frog sheet schema follows standard export patterns
* Google Sheets access remains publicly readable

### Limitations

* GA4 calculated metrics are limited to supported API fields
* SEO logic currently focuses on technical SEO attributes
* No persistent storage (stateless by design)

