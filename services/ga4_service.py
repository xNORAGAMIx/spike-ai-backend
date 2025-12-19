from google.analytics.data_v1beta import BetaAnalyticsDataClient # type: ignore
from google.analytics.data_v1beta.types import RunReportRequest # type: ignore


METRIC_ALIASES = {
    "pageViews": "screenPageViews",
    "pageviews": "screenPageViews",
    "views": "screenPageViews",
    "page_views": "screenPageViews",
    "users": "totalUsers",
    "userCount": "totalUsers",
    "sessions": "sessions"
}

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

    raw_metrics = plan.get("metrics", [])

    normalized_metrics = []

    for m in raw_metrics:
        # Direct match
        if m in ALLOWED_METRICS:
            normalized_metrics.append({"name": m})

        # Alias match
        elif m in METRIC_ALIASES:
            alias = METRIC_ALIASES[m]
            if alias in ALLOWED_METRICS:
                normalized_metrics.append({"name": alias})


    dimensions = [
        {"name": d} for d in plan.get("dimensions", [])
        if d in ALLOWED_DIMENSIONS
    ]

    raw_range = plan.get("date_range", {})

    date_range = {
        "start_date": raw_range.get("start", "7daysAgo"),
        "end_date": raw_range.get("end", "today")
    }

    if not normalized_metrics:
        raise ValueError(
            f"No valid GA4 metrics after validation. Requested: {raw_metrics}"
        )

    request = RunReportRequest(
        property=f"properties/{property_id}",
        metrics=normalized_metrics,
        dimensions=dimensions,
        date_ranges=[date_range]
    )

    response = client.run_report(request)
    return response

# done