import sys
from anime_quotes.quotes import get_quote_by_author, random_quote

def main():
    if len(sys.argv) > 1:
        search = " ".join(sys.argv[1:]).lower()
        quote_data = get_quote_by_author(search)

        if quote_data:
            print(f'"{quote_data["quote"]}" - {quote_data["author"]}')
        else:
            print(f'❌ Quote dengan author mengandung "{search}" tidak ditemukan.')
    else:
        print(random_quote())
