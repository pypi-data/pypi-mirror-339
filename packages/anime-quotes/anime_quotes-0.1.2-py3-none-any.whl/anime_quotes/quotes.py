import random
import requests
import os
import json

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

def random_quote(author=None):
    url = "https://raw.githubusercontent.com/miya3333/anime-quotes-data/refs/heads/main/quotes.json"
    
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        quotes = response.json()
        cache_quotes(quotes)
    except Exception as e:
        quotes = get_cached_quotes()
        if not quotes:
            return (
                "⚠️  Failed to load quotes from GitHub and no cached data found.\n"
                "Please connect to the internet and try again.\n"
                f"Error: {e}"
            )

    if author:
        filtered = [q for q in quotes if q["author"].lower() == author.lower()]
        if not filtered:
            return f"No quotes found for author: {author}"
        quote = random.choice(filtered)
    else:
        quote = random.choice(quotes)

    return f'"{quote["quote"]}" – {quote["author"]}'
