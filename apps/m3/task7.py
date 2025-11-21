import os
from bs4 import BeautifulSoup, SoupReplacer
'''The attrs_xformer contract mandates it returns the tag's final attribute dictionary.

Returning an empty dictionary ({}) signals the tag must possess zero attributes.

The tag.attrs = {} assignment instantly overwrites and clears all pre-existing attributes on the Tag instance.

'''


def attribute_whitelist_xformer(tag):
    """
    An attrs_xformer function.
    
    It preserves 'href' for <a> tags and 'src' for <img> tags.
    It removes all other attributes from all other tags.
    
    It must *return* a new attribute dictionary.
    """
    
    # Start with an empty dict
    new_attrs = {}
    
    # Check the whitelist conditions
    if tag.name == 'a' and 'href' in tag.attrs:
        new_attrs['href'] = tag.attrs['href']
    elif tag.name == 'img' and 'src' in tag.attrs:
        new_attrs['src'] = tag.attrs['src']
    
    # For all other tags, and <a>/<img> tags that don't match,
    # the empty new_attrs dict will be returned,
    # effectively stripping them of all attributes.
    
    return new_attrs

# --- Main Program ---
if __name__ == "__main__":
    
    # 1. Create the SoupReplacer
    # We only use the attrs_xformer
    attr_stripper = SoupReplacer(attrs_xformer=attribute_whitelist_xformer)

    # 2. Find and read the HTML file
    # (Assuming test.html is in the same directory as this script)
    script_dir = os.path.dirname(__file__)
    if not script_dir:
        script_dir = "."
        
    file_path = os.path.join(script_dir, "test.html")

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            html_doc = f.read()
    except FileNotFoundError:
        print(f"Error: File not found {file_path}")
        print("Please ensure 'test.html' is in the same directory as task7.py.")
        exit(1)

    print("--- Original HTML (Snippet) ---")
    print("\n".join(html_doc.splitlines()[6:18])) # Print a snippet

    # 3. Parse the document using the replacer
    # The replacer does all the work during parsing
    soup = BeautifulSoup(html_doc, "html.parser", replacer=attr_stripper)

    print("\n" + "="*30 + "\n")
    print("--- Transformed HTML (Prettified) ---")
    
    # 4. Print the result
    # Note that all attributes (class, id, style, target, etc.) are gone,
    # leaving only <a>.href and <img>.src
    print(soup.prettify())

    # Validation
    print("\n--- Validation ---")
    a_tag = soup.find('a')
    print(f"First <a> tag: {a_tag}")
    print(f"Its attributes: {a_tag.attrs}")
    assert a_tag.attrs == {'href': 'story1.html'}
    
    img_tag = soup.find('img')
    print(f"First <img> tag: {img_tag}")
    print(f"Its attributes: {img_tag.attrs}")
    assert img_tag.attrs == {'src': 'image1.jpg'}
    
    p_tag = soup.find('p')
    print(f"First <p> tag: {p_tag}")
    print(f"Its attributes: {p_tag.attrs}")
    assert p_tag.attrs == {}
    
    print("\nTask 7 completed successfully!")