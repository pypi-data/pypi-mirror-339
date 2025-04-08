import sys
from . import random_quote

def main():
    author = sys.argv[1] if len(sys.argv) > 1 else None
    print(random_quote(author))
