#!/usr/bin/env python3

import sys
import os
import time
import xml.etree.ElementTree as ET

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def extract_urls_from_sitemap(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    ns = root.tag.split("}")[0].lstrip("{") if "}" in root.tag else ""
    prefix = f"{{{ns}}}" if ns else ""
    urls = [loc.text.strip() for loc in root.iter(f"{prefix}loc") if loc.text]
    return urls


def slugify(url):
    url = url.rstrip("/")
    name = url.split("//", 1)[-1].replace("/", "_").replace(":", "_")
    return name[:120]


def make_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument(
        "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)


def scrape(xml_path):
    urls = extract_urls_from_sitemap(xml_path)
    if not urls:
        print("No URLs found in sitemap.")
        return

    output_dir = os.path.dirname(os.path.abspath(xml_path))
    print(f"Found {len(urls)} URLs. Saving output to: {output_dir}\n")

    driver = make_driver()

    try:
        for url in urls:
            print(f"Fetching: {url}")
            try:
                driver.get(url)
                time.sleep(2)  # let JS render

                soup = BeautifulSoup(driver.page_source, "html.parser")

                title = soup.title.get_text(strip=True) if soup.title else ""

                for tag in soup(["script", "style", "noscript", "header", "footer", "nav"]):
                    tag.decompose()

                body = soup.find("body")
                body_text = body.get_text(separator="\n", strip=True) if body else ""

                filename = slugify(url) + ".txt"
                filepath = os.path.join(output_dir, filename)

                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(f"URL: {url}\n")
                    f.write(f"TITLE: {title}\n")
                    f.write("=" * 60 + "\n")
                    f.write(body_text)

                print(f"  Saved: {filename}\n")

            except Exception as e:
                print(f"  ERROR: {e}\n")

    finally:
        driver.quit()

    print("Done.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 scraper.py <sitemap.xml>")
        sys.exit(1)
    scrape(sys.argv[1])
