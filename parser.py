from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
from typing import List, Tuple, Optional


def extract_items(html: str, base_url: str, selector: Optional[str] = None,
include_regex: Optional[str] = None, exclude_regex: Optional[str] = None) -> List[Tuple[str, str]]:
"""
Vrátí list (title, absolute_url). Pokud je dán CSS selektor, omezí se na jeho obsah.
Pokud je dán include/exclude regex, filtruje výsledky podle URL nebo textu.
"""
soup = BeautifulSoup(html, "lxml")
root = soup.select_one(selector) if selector else soup

anchors = []
# klasicky všechny odkazy
for a in root.select("a"):
text = a.get_text(strip=True)
href = a.get("href")
if not href or not text:
continue
anchors.append((text, urljoin(base_url, href)))

for tag in root.select("[data-product-name], img[alt], [title]"):
href = tag.get("href") or tag.get("data-url") or None
if not href:
continue
text = tag.get("data-product-name") or tag.get("title") or tag.get("alt") or ""
if not text:
continue
anchors.append((text.strip(), urljoin(base_url, href)))

# odfiltrování duplicit
dedup = {}
for t, h in anchors:
key = (t.strip(), h.strip())
dedup[key] = key
items = list(dedup.keys())

# regexy
if include_regex:
inc = re.compile(include_regex, re.IGNORECASE)
items = [(t, h) for t, h in items if inc.search(t) or inc.search(h)]
if exclude_regex:
exc = re.compile(exclude_regex, re.IGNORECASE)
items = [(t, h) for t, h in items if not (exc.search(t) or exc.search(h))]

return items
