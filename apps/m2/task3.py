
import sys
from bs4 import BeautifulSoup, SoupStrainer

if len(sys.argv) < 2:
    print("Usage: python task3.py <html_file>")
    sys.exit(1)

file_path = sys.argv[1]

# 1. Define SoupStrainer: Match all tags (True as the first argument)
# This effectively tells the parser to process all tags, serving as a baseline.
all_elements = SoupStrainer(True)

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        # 2. Parse the entire document using the SoupStrainer
        soup = BeautifulSoup(f, 'html.parser', parse_only=all_elements)

    print(f"--- All Tags in {file_path} ---")

    # Find all tags using find_all(True)
    all_tags = soup.find_all(True)

    # Count tag occurrences
    tag_names = {}
    for tag in all_tags:
        tag_names[tag.name] = tag_names.get(tag.name, 0) + 1

    print(f"Total unique tags: {len(tag_names)}")
    print("Tag counts:")
    for name, count in sorted(tag_names.items()):
        print(f"  <{name}>: {count}")

except FileNotFoundError:
    print(f"Error: File not found at {file_path}")