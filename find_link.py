import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def find_download_link(page_url):
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(page_url, headers=headers, timeout=20)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    candidates = []

    for a in soup.find_all("a", href=True):
        text = (a.get_text(strip=True) or "").replace(
            "\u200c", "")
        if re.search(r"320", text) or "دانلود" in text and "320" in text:
            href = a["href"]
            full = urljoin(page_url, href)
            candidates.append(full)

    for a in soup.find_all("a", href=True):
        href = a["href"]
        full = urljoin(page_url, href)
        if full.lower().endswith(".mp3"):
            candidates.append(full)

    uniq = []
    seen = set()
    for url in candidates:
        if url not in seen:
            seen.add(url)
            uniq.append(url)

    prio = [u for u in uniq if u.lower().endswith(".mp3") and "320" in u]
    if prio:
        return prio[0]
    prio2 = [u for u in uniq if u.lower().endswith(".mp3")]
    if prio2:
        return prio2[0]

    for tag in soup.select("[data-url]"):
        full = urljoin(page_url, tag.get("data-url"))
        if full.lower().endswith(".mp3"):
            return full

    for tag in soup.select("[onclick]"):
        oc = tag.get("onclick", "")
        m = re.search(r"['\"](https?://[^'\"]+\.mp3)['\"]", oc)
        if m:
            return m.group(1)

    return None
