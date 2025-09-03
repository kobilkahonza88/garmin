import os
from urllib.parse import urljoin
from typing import Tuple

import requests
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

USE_PLAYWRIGHT = os.getenv("USE_PLAYWRIGHT", "false").lower() in {"1", "true", "yes"}

DEFAULT_HEADERS = {
"User-Agent": (
"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
"(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
),
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
"Accept-Language": "en-US,en;q=0.9",
}

class FetchError(Exception):
pass


@retry(reraise=True,
stop=stop_after_attempt(3),
wait=wait_exponential(multiplier=1, min=1, max=10),
retry=retry_if_exception_type((requests.RequestException, FetchError)))
def _fetch_requests(url: str) -> Tuple[str, str]:
resp = requests.get(url, headers=DEFAULT_HEADERS, timeout=15, allow_redirects=True)
if resp.status_code >= 400:
raise FetchError(f"HTTP {resp.status_code} for {url}")
final_url = resp.url
return resp.text, final_url


def _fetch_playwright(url: str) -> Tuple[str, str]:
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
browser = p.chromium.launch(headless=True)
context = browser.new_context()
page = context.new_page()
page.set_extra_http_headers(DEFAULT_HEADERS)
page.goto(url, wait_until="networkidle", timeout=30000)
html = page.content()
final_url = page.url
context.close()
browser.close()
return html, final_url


def fetch_html(url: str) -> Tuple[str, str]:
if USE_PLAYWRIGHT:
return _fetch_playwright(url)
return _fetch_requests(url)
