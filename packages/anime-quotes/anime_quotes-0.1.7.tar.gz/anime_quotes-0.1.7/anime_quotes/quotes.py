import random
import requests
import os
import json
import re

def normalize(text):
    return re.sub(r'[^a-zA-Z0-9]', '', text.lower())

def get_cached_quotes():
    cache_file = os.path.join(os.path.expanduser("~"), ".anime_quotes_cache.json")
    if os.path.exists(cache_file):
        with open(cache_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def cache_quotes(quotes):
    cache_file = os.path.join(os.path.expanduser("~"), ".anime_quotes_cache.json")
    with open(cache_file, "w", encoding="utf-8") as f:
        json.dump(quotes, f)

def fetch_quotes():
    url = "https://raw.githubusercontent.com/miya3333/anime-quotes-data/refs/heads/main/quotes.json"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        quotes = response.json()
        cache_quotes(quotes)
    except Exception:
        quotes = get_cached_quotes()
        if not quotes:
            return None
    return quotes

def random_quote(author=None):
    quotes = fetch_quotes()
    if quotes is None:
        return (
            "⚠️  Failed to load quotes from GitHub and no cached data found.\n"
            "Please connect to the internet and try again."
        )

    if author:
        norm_author = normalize(author)
        filtered = [q for q in quotes if norm_author in normalize(q["author"])]
        if not filtered:
            return f"❌ No quotes found for author matching: '{author}'"
        quote = random.choice(filtered)
    else:
        quote = random.choice(quotes)

    return f'"{quote["quote"]}" – {quote["author"]}'

def get_quote_by_author(author):
    quotes = fetch_quotes()
    if quotes is None:
        return None

    norm_author = normalize(author)
    filtered = [q for q in quotes if norm_author in normalize(q["author"])]
    if not filtered:
        return None
    return random.choice(filtered)
