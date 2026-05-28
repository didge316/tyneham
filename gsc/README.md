# GSC Export — tynehamvillage.org

Pulls last full calendar month from Google Search Console and saves to `data/YYYY-MM.csv`.

## One-time setup

### 1. Install dependencies

```bash
pip install google-auth-oauthlib google-api-python-client
```

### 2. Create OAuth credentials in Google Cloud Console

1. Go to [console.cloud.google.com](https://console.cloud.google.com)
2. Create a new project (or reuse one) → **APIs & Services → Library**
3. Search for **Google Search Console API** and enable it
4. Go to **APIs & Services → Credentials → Create Credentials → OAuth client ID**
5. Application type: **Desktop app**
6. Download the JSON file and save it as `credentials.json` in this directory

### 3. Add yourself as a test user (if the app is in testing mode)

**APIs & Services → OAuth consent screen → Test users** — add your Google account email.

### 4. Run

```bash
cd /home/matt/claude/websites/tyneham/gsc
python3 gsc_export.py
```

A browser window opens on the first run for OAuth. After approving, `token.json` is saved — future runs are silent.

## Output

`data/YYYY-MM.csv` — one file per month, columns:

| column | description |
|--------|-------------|
| query | search term |
| page | full URL of the page that appeared |
| clicks | number of clicks |
| impressions | number of times shown in results |
| ctr | click-through rate (e.g. 0.0312 = 3.12%) |
| position | average ranking position |

## Notes

- `credentials.json` and `token.json` are gitignored — never commit them
- Running the script again for the same month overwrites the existing CSV
- GSC data has a 2–3 day lag, so data for the last day of the month may not be complete until ~3rd of the next month
