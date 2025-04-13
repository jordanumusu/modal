import requests
from bs4 import BeautifulSoup
from urllib.parse import quote, urlparse
import re

def search_duckduckgo(query: str):
    search_url = f"https://duckduckgo.com/html/?q={quote(query)}"
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_2 like Mac OS X)"
    }
    res = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    for a in soup.select("a.result__a"):
        href = a.get("href")
        if "tabs.ultimate-guitar.com/tab/" in href:
            return href
    return None

def fetch_chords_sectioned(url: str):
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_2 like Mac OS X)"
    }
    parsed = urlparse(url)
    mobile_url = f"https://tabs.ultimate-guitar.com{parsed.path}"
    res = requests.get(mobile_url, headers=headers)
    soup = BeautifulSoup(res.content, "html.parser")
    content = soup.find("pre", class_="extra")

    if not content:
        return {"Error": ["No chord block found."]}

    lines = content.get_text().splitlines()
    result = {}
    current_section = "Unknown"

    for line in lines:
        section_match = re.match(r"\[(.*?)\]", line.strip())
        if section_match:
            current_section = section_match.group(1).strip()
            result[current_section] = []
        else:
            chords = re.findall(r"[A-G][#b]?(?:m|maj|min|dim|aug|sus)?\d*", line)
            if chords:
                result.setdefault(current_section, []).extend(chords)

    return result
