def fuse_analytics_seo(analytics_rows, seo_rows, limit=10):
    seo_map = {
        row.get("url") or row.get("page"): row
        for row in seo_rows
    }

    fused = []
    for row in analytics_rows[:limit]:
        path = row.get("pagePath")
        seo = seo_map.get(path, {})

        fused.append({
            "page": path,
            "views": row.get("screenPageViews"),
            "title": seo.get("title", "Not available"),
            "indexability": seo.get("indexability", "Unknown")
        })

    return fused

# done