"""
Crawler module:
- Fetch .onion pages over Tor
- Perform controlled multi-page crawling
- Extract visible text and darknet links only
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from config import TOR_PROXY, REQUEST_TIMEOUT


HEADERS = {
    "User-Agent": "Mozilla/5.0 DarkWebMonitor/1.0"
}


def fetch(url):
    """Fetch a URL over Tor. Returns HTML or None."""
    try:
        r = requests.get(
            url,
            proxies=TOR_PROXY,
            timeout=REQUEST_TIMEOUT,
            headers=HEADERS
        )
        r.raise_for_status()
        return r.text
    except Exception:
        return None


def extract_text_and_links(base_url, html):
    """Extract visible text and .onion links from HTML."""
    soup = BeautifulSoup(html, "lxml")

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    text = soup.get_text(separator=" ", strip=True)

    links = set()
    for a in soup.find_all("a", href=True):
        full_url = urljoin(base_url, a["href"])
        if ".onion" in full_url:
            links.add(full_url)

    return text, links


def crawl(start_url, max_pages=20):
    """
    Crawl multiple darknet pages starting from a seed URL.
    Returns list of:
    {
        url: str,
        text: str,
        links: list
    }
    """
    visited = set()
    queue = [start_url]
    pages = []

    while queue and len(visited) < max_pages:
        url = queue.pop(0)

        if url in visited:
            continue

        html = fetch(url)
        if not html:
            continue

        text, links = extract_text_and_links(url, html)

        visited.add(url)
        pages.append({
            "url": url,
            "text": text,
            "links": list(links)
        })

        for link in links:
            if link not in visited:
                queue.append(link)

    return pages

