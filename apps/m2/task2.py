
import sys
from bs4 import BeautifulSoup, SoupStrainer

# Check for command line argument
if len(sys.argv) < 2:
    print("Usage: python task2.py <html_file>")
    sys.exit(1)

file_path = sys.argv[1]

# 1. Define SoupStrainer: Only interested in 'a' tags
# Syntax: SoupStrainer(name, attrs={}, text=None, **kwargs)
only_a_tags = SoupStrainer('a')

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        # 2. Pass SoupStrainer to the 'parse_only' parameter of BeautifulSoup
        # BeautifulSoup will only build the tree with 'a' tags and their contents.
        soup = BeautifulSoup(f, 'html.parser', parse_only=only_a_tags)

    print(f"--- Hyperlinks in {file_path} (Parsed via SoupStrainer) ---")

    # Since the strainer has already filtered the document, this is very fast.
    all_links = soup.find_all('a')

    for link in all_links:
        # Retrieve the 'href' attribute safely
        href = link.get('href', 'NO HREF')
        print(f"Text: {link.get_text()} | Href: {href}")

    print(f"Total 'a' tags found: {len(all_links)}")

except FileNotFoundError:
    print(f"Error: File not found at {file_path}")