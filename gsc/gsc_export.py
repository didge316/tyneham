#!/home/matt/claude/.venv/bin/python3
"""
gsc_export.py — Export Google Search Console data to CSV.

Default: last full calendar month.
--current: current month so far (1st to yesterday).

Output: data/YYYY-MM.csv  (query, page, clicks, impressions, ctr, position)
"""

import argparse
import csv
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
OUTPUT_DIR = SCRIPT_DIR / "data"
ROW_LIMIT = 25_000


def last_full_month():
    first_of_this_month = date.today().replace(day=1)
    last_day = first_of_this_month - timedelta(days=1)
    return last_day.replace(day=1).isoformat(), last_day.isoformat()


def current_month_so_far():
    today = date.today()
    start = today.replace(day=1)
    end = today - timedelta(days=1)  # GSC has ~2 day lag
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


def fetch_rows(service, start_date, end_date):
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
                    "dimensions": ["query", "page"],
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


def write_csv(rows, start_date):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    month = start_date[:7]  # YYYY-MM
    path = OUTPUT_DIR / f"{month}.csv"
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["query", "page", "clicks", "impressions", "ctr", "position"])
        for row in rows:
            q, page = row["keys"]
            writer.writerow([
                q,
                page,
                row["clicks"],
                row["impressions"],
                round(row["ctr"], 4),
                round(row["position"], 1),
            ])
    return path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--current", action="store_true", help="Export current month so far instead of last full month")
    args = parser.parse_args()

    start_date, end_date = current_month_so_far() if args.current else last_full_month()
    print(f"Fetching {start_date} → {end_date} ...")

    service = build("searchconsole", "v1", credentials=authenticate())
    rows = fetch_rows(service, start_date, end_date)
    print(f"  {len(rows):,} rows")

    path = write_csv(rows, start_date)
    print(f"  Saved: {path}")


if __name__ == "__main__":
    main()
