from google.analytics.data_v1beta import BetaAnalyticsDataClient # type: ignore
from google.analytics.data_v1beta.types import RunReportRequest # type: ignore

# SAFE allowlists (minimal but valid)
ALLOWED_METRICS = {
    "screenPageViews",
    "totalUsers",
    "sessions",
    "eventCount"
}

ALLOWED_DIMENSIONS = {
    "date",
    "pagePath",
    "sessionSource",
    "country",
    "deviceCategory"
}

def run_ga4_report(property_id: str, plan: dict):
    client = BetaAnalyticsDataClient.from_service_account_file(
        "credentials.json"
    )

    metrics = [
        {"name": m} for m in plan.get("metrics", [])
        if m in ALLOWED_METRICS
    ]

    dimensions = [
        {"name": d} for d in plan.get("dimensions", [])
        if d in ALLOWED_DIMENSIONS
    ]

    date_range = plan.get("date_range", {
        "start": "7daysAgo",
        "end": "today"
    })

    if not metrics:
        raise ValueError("No valid GA4 metrics after validation")

    request = RunReportRequest(
        property=f"properties/{property_id}",
        metrics=metrics,
        dimensions=dimensions,
        date_ranges=[date_range]
    )

    response = client.run_report(request)
    return response
