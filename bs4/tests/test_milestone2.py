# test_milestone2.py

"""
Unit tests for Milestone 2 tasks: 
Task 2/4 (Filtering), Task 3 (Structure), and Task 6 (HTML Replacer basic functionality).
"""

import unittest
import sys
import os # Included for path resolution (for reference, though not strictly used in tests)
import time
from bs4 import BeautifulSoup, SoupReplacer, SoupStrainer 

# 
TEST_MARKUP = """
<html>
<head>
    <title id="doc-title">Test Document</title>
</head>
<body>
    <a href="link1.html">Link One</a>
    <div id="main-content" class="container">
        <p>A paragraph with <b>bold text 1</b>.</p>
        <a href="link2.html" class="internal-link">Link Two</a>
        <span id="data-point">Data</span>
    </div>
    <b class="warning-text">bold text 2</b>
    <i class="icon"></i>
</body>
</html>
"""

class TestMilestone2HTML(unittest.TestCase):
    """
    Tests core Beautiful Soup functionality and custom Replacer logic for HTML parsing.
    """
    
    def setUp(self):
        """Prepare a clean BeautifulSoup instance for each test."""
        self.soup = BeautifulSoup(TEST_MARKUP, "html.parser")

    # --- Task 2 & 4 Logic Tests (Filtering / SoupStrainer) ---

    def test_task2_find_all_a_tags(self):
        """Verify Task 2: Finding all <a> tags."""
        a_tags = self.soup.find_all('a')
        self.assertEqual(len(a_tags), 2, "Task 2: Expected 2 <a> tags.")

    def test_task4_find_tags_with_id_attribute(self):
        """Verify Task 4: Finding all tags containing the 'id' attribute."""
        tags_with_id = self.soup.find_all(id=True)
        self.assertEqual(len(tags_with_id), 3, "Task 4: Expected 3 tags with 'id' attribute.")
        
        # Verify specific ID values
        ids = sorted([t['id'] for t in tags_with_id])
        self.assertEqual(ids, ['data-point', 'doc-title', 'main-content'], "Extracted ID attributes should match expected list.")

    # --- Task 3 Logic Test (Structure) ---

    def test_task3_count_unique_tags(self):
        """Verify Task 3: The parser correctly builds the full tree structure."""
        unique_tags = {tag.name for tag in self.soup.find_all(True) if tag.name is not None}
        expected_tags = {'html', 'head', 'title', 'body', 'a', 'div', 'p', 'b', 'span', 'i'}
        
        # We need to account for potential tags added by the parser (like 'link' or 'br')
        # Here we only check that the primary structural tags are present
        missing_tags = expected_tags - unique_tags
        self.assertFalse(missing_tags, f"Task 3: Missing expected tags: {missing_tags}")
        

    # --- Task 6 Logic Test (Basic HTML Replacer) ---

    def test_task6_html_replacement_basic_functionality(self):
        """Verify Task 6: Tag replacement (<b> -> <blockquote>) is successful with basic markup."""
        # Define replacement rule
        b_to_blockquote = SoupReplacer("b", "blockquote")
        
        # Parse using the replacer
        soup = BeautifulSoup(TEST_MARKUP, 'html.parser', replacer=b_to_blockquote)

        # 1. Verify original tag <b> is gone
        self.assertIsNone(soup.find('b'), "Original 'b' tag should be replaced and gone.")

        # 2. Verify replaced tag <blockquote> appears
        blockquotes = soup.find_all('blockquote')
        self.assertEqual(len(blockquotes), 2, "Expected 2 replaced <blockquote> tags.")

        # 3. Verify content and attributes are preserved
        self.assertEqual(blockquotes[0].text, "bold text 1", "Content of the first tag must be preserved.")
        self.assertIn('warning-text', blockquotes[1]['class'], "Attributes must be preserved on the new tag.")


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)