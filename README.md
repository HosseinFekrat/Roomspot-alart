import os
import json
import requests
from bs4 import BeautifulSoup

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

URL = "https://www.roomspot.nl/aanbod/te-huur"
STATE_FILE = "seen.json"

def send_message(message):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": message},
        timeout=30
    ).raise_for_status()

def get_listings():
    response = requests.get(
        URL,
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=30
    )
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    listings = {}
    for link in soup.find_all("a", href=True):
        href = link["href"]
        title = link.get_text(" ", strip=True)

        if not title or "/aanbod/" not in href:
            continue

        full_url = requests.compat.urljoin(URL, href)
        if "enschede" in (title + " " + href).lower():
            listings[full_url] = title

    return listings

def main():
    listings = get_listings()

    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, encoding="utf-8") as f:
            seen = json.load(f)
    else:
        seen = []

    new_items = {
        url: title for url, title in listings.items()
        if url not in seen
    }

    for url, title in new_items.items():
        send_message(f"آگهی جدید Roomspot در Enschede:\n{title}\n{url}")

    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(list(listings.keys()) + seen, f)

if name == "__main__":
    main()
