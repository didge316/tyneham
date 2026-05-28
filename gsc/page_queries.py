#!/home/matt/claude/.venv/bin/python3
"""
page_queries.py — Pull per-page query data from GSC for specific URLs.

Usage:
    python3 page_queries.py --start 2026-02-26 --end 2026-05-25

Outputs top 20 queries by impressions and by clicks for each target page.
"""

import argparse
import json
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

TARGET_PAGES = [
    "https://tynehamvillage.org/ghost-village",
    "https://tynehamvillage.org/history-of-tyneham",
]


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


def fetch_page_queries(service, page_url, start_date, end_date, row_limit=25000):
    """Fetch all queries for a specific page URL."""
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
                    "rowLimit": row_limit,
                    "startRow": start_row,
                },
            )
            .execute()
        )
        batch = response.get("rows", [])
        rows.extend(batch)
        if len(batch) < row_limit:
            break
        start_row += row_limit
    return rows


def print_table(title, rows, sort_key, top_n=20):
    print(f"\n{title}")
    print("-" * 70)
    sorted_rows = sorted(rows, key=lambda r: r[sort_key], reverse=True)[:top_n]
    print(f"{'Query':<45} {'Clicks':>7} {'Impr':>7} {'CTR':>6} {'Pos':>6}")
    print(f"{'-----':<45} {'------':>7} {'----':>7} {'---':>6} {'---':>6}")
    for r in sorted_rows:
        query = r["keys"][0][:44]
        clicks = r["clicks"]
        impressions = r["impressions"]
        ctr = f"{r['ctr']*100:.1f}%"
        position = f"{r['position']:.1f}"
        print(f"{query:<45} {clicks:>7} {impressions:>7} {ctr:>6} {position:>6}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", default="2026-02-26", help="Start date YYYY-MM-DD")
    parser.add_argument("--end", default="2026-05-25", help="End date YYYY-MM-DD")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    args = parser.parse_args()

    print(f"Authenticating ...")
    service = build("searchconsole", "v1", credentials=authenticate())

    results = {}
    for page_url in TARGET_PAGES:
        print(f"Fetching queries for: {page_url} ({args.start} → {args.end}) ...")
        rows = fetch_page_queries(service, page_url, args.start, args.end)
        results[page_url] = rows
        print(f"  {len(rows)} queries found")

    if args.json:
        print(json.dumps(results, indent=2))
        return

    for page_url, rows in results.items():
        print(f"\n{'='*70}")
        print(f"PAGE: {page_url}")
        print(f"Date range: {args.start} to {args.end}  |  Total queries: {len(rows)}")
        print(f"{'='*70}")

        if not rows:
            print("  No data returned for this page.")
            continue

        print_table("TOP 20 BY IMPRESSIONS", rows, "impressions", top_n=20)
        print_table("TOP 20 BY CLICKS", rows, "clicks", top_n=20)


if __name__ == "__main__":
    main()
