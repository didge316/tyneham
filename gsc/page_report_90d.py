#!/home/matt/claude/.venv/bin/python3
"""
page_report_90d.py — GSC page-level performance for last 90 days.

Fetches:
  1. All pages: clicks, impressions, avg position (aggregated, sorted by impressions desc)
  2. Top 3 queries for each of the top 15 pages by impressions

Outputs JSON to stdout.
"""

import json
from datetime import date, timedelta
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SITE_URL = "sc-domain:tynehamvillage.org"
SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]
SCRIPT_DIR = Path(__file__).parent
CREDENTIALS_FILE = SCRIPT_DIR / "credentials.json"
TOKEN_FILE = SCRIPT_DIR / "token.json"
ROW_LIMIT = 25_000


def date_range_90():
    end = date.today() - timedelta(days=3)   # GSC lag
    start = end - timedelta(days=89)
    return start.isoformat(), end.isoformat()


def authenticate():
    creds = None
    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        TOKEN_FILE.write_text(creds.to_json())
    return creds


def fetch_pages(service, start_date, end_date):
    """Fetch all pages aggregated: clicks, impressions, position."""
    rows = []
    start_row = 0
    while True:
        response = (
            service.searchanalytics()
            .query(
                siteUrl=SITE_URL,
                body={
                    "startDate": start_date,
                    "endDate": end_date,
                    "dimensions": ["page"],
                    "rowLimit": ROW_LIMIT,
                    "startRow": start_row,
                },
            )
            .execute()
        )
        batch = response.get("rows", [])
        rows.extend(batch)
        if len(batch) < ROW_LIMIT:
            break
        start_row += ROW_LIMIT
    return rows


def fetch_queries_for_page(service, page_url, start_date, end_date, top_n=3):
    """Fetch top N queries by impressions for a specific page."""
    response = (
        service.searchanalytics()
        .query(
            siteUrl=SITE_URL,
            body={
                "startDate": start_date,
                "endDate": end_date,
                "dimensions": ["query"],
                "dimensionFilterGroups": [
                    {
                        "filters": [
                            {
                                "dimension": "page",
                                "operator": "equals",
                                "expression": page_url,
                            }
                        ]
                    }
                ],
                "rowLimit": top_n,
                "orderBy": [{"fieldName": "impressions", "sortOrder": "DESCENDING"}],
            },
        )
        .execute()
    )
    return response.get("rows", [])


def main():
    start_date, end_date = date_range_90()
    import sys
    print(f"Date range: {start_date} to {end_date}", file=sys.stderr)

    service = build("searchconsole", "v1", credentials=authenticate())

    print("Fetching all pages...", file=sys.stderr)
    page_rows = fetch_pages(service, start_date, end_date)
    print(f"  {len(page_rows)} pages found", file=sys.stderr)

    # Sort by impressions descending
    page_rows.sort(key=lambda r: r["impressions"], reverse=True)

    pages_data = []
    for r in page_rows:
        pages_data.append({
            "url": r["keys"][0],
            "clicks": r["clicks"],
            "impressions": r["impressions"],
            "avg_position": round(r["position"], 1),
        })

    top15 = pages_data[:15]

    print("Fetching top 3 queries for top 15 pages...", file=sys.stderr)
    top_page_queries = {}
    for p in top15:
        url = p["url"]
        print(f"  {url}", file=sys.stderr)
        q_rows = fetch_queries_for_page(service, url, start_date, end_date, top_n=3)
        queries = []
        for qr in q_rows:
            queries.append({
                "query": qr["keys"][0],
                "clicks": qr["clicks"],
                "impressions": qr["impressions"],
                "avg_position": round(qr["position"], 1),
            })
        top_page_queries[url] = queries

    output = {
        "date_range": {"start": start_date, "end": end_date},
        "pages": pages_data,
        "top_page_queries": top_page_queries,
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
