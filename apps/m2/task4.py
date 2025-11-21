# task4.py
import sys
from bs4 import BeautifulSoup, SoupStrainer

if len(sys.argv) < 2:
    print("Usage: python task4.py <html_file>")
    sys.exit(1)

file_path = sys.argv[1]

# 1. Define SoupStrainer: Match any tag (True) that has an 'id' attribute
# {'id': True} means the 'id' attribute must be present, regardless of its value.
tags_with_id = SoupStrainer(True, {'id': True})

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        # 2. Parse the file. Only tags with 'id' will be included in the soup object.
        soup = BeautifulSoup(f, 'html.parser', parse_only=tags_with_id)

    print(f"--- Tags with 'id' attribute in {file_path} (Parsed via SoupStrainer) ---")

    # 3. Single API call (find_all(True)) to retrieve all parsed elements.
    # Since the SoupStrainer already filtered the tags, this list only contains tags with 'id'.
    found_elements = soup.find_all(True, id=True)# update, use id=True to make sure every tag contains the id

    for element in found_elements:
        # Access the 'id' attribute using dictionary-style lookup
        print(f"Tag: <{element.name}> | ID: {element['id']}")

    print(f"Total tags with 'id' found: {len(found_elements)}")

except FileNotFoundError:
    print(f"Error: File not found at {file_path}")