import os
for site in cfg["sites"]:
interval = int(site.get("interval", DEFAULT_POLL_SECONDS))
schedule[site["name"]] = now - interval # ať se vše spustí hned na začátku

while running:
loop_start = time.time()
for site in cfg["sites"]:
name = site["name"]
interval = int(site.get("interval", DEFAULT_POLL_SECONDS))
due = loop_start - schedule[name] >= interval
if not due:
continue

url = site["url"]
keywords = site.get("keywords", [])
selector = site.get("selector")
include_regex = site.get("include_regex")
exclude_regex = site.get("exclude_regex")

try:
logger.info("[%s] Fetching %s", name, url)
html, final_url = fetch_html(url)
items = extract_items(html, base_url=final_url, selector=selector,
include_regex=include_regex, exclude_regex=exclude_regex)
logger.info("[%s] Parsed %d candidate items", name, len(items))

found_new = []
for title, href in items:
text = f"{title} {href}".lower()
if keywords and not any(k.lower() in text for k in keywords):
continue
key = f"{name}|{href}|{title.lower()}"
if not has_seen(key):
mark_seen(key, title, href, name)
found_new.append((title, href))

for title, link in found_new:
msg = f"🆕 {name}\n{title}\n{link}"
notify(msg)
logger.info("[%s] NEW: %s", name, title)

except Exception as e:
logger.exception("[%s] Error: %s", name, e)
try:
notify(f"⚠️ Chyba při kontrole {name}: {e}")
except Exception:
logger.error("Failed to notify about error.")
finally:
schedule[name] = time.time()
time.sleep(random.uniform(0.5, 1.5))

time.sleep(3)


if __name__ == "__main__":
main()
