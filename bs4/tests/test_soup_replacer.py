import unittest
from bs4 import BeautifulSoup, SoupReplacer

class TestSoupReplacer(unittest.TestCase):
    """
    Tests for the SoupReplacer functionality (Milestones 2 and 3).
    """

    # --- Milestone 3 Tests ---

    def test_m3_name_xformer(self):
        # Test Case 1: Using name_xformer (b -> blockquote example)
        html = "<p><b>Hello</b> World</p>"
        b_to_blockquote = SoupReplacer(
            name_xformer=lambda tag: "blockquote" if tag == "b" else tag
        )
        soup = BeautifulSoup(html, "html.parser", replacer=b_to_blockquote)
        
        self.assertIsNone(soup.b)
        self.assertIsNotNone(soup.blockquote)
        self.assertEqual(soup.blockquote.name, "blockquote")
        self.assertEqual(soup.blockquote.string, "Hello")
        self.assertEqual(str(soup), "<p><blockquote>Hello</blockquote> World</p>")

    def test_m3_xformer_side_effect(self):
        # Test Case 2: Using xformer for in-place modification (remove_class_attr example)
        html = '<p class="foo" id="bar">Hello</p><span class="foo">Bye</span>'
        
        def remove_class_attr(tag):
            if "class" in tag.attrs:
                del tag.attrs["class"]
                
        class_deleter = SoupReplacer(xformer=remove_class_attr)
        soup = BeautifulSoup(html, "html.parser", replacer=class_deleter)
        
        self.assertEqual(str(soup), '<p id="bar">Hello</p><span>Bye</span>')
        self.assertEqual(soup.p.attrs, {"id": "bar"})
        self.assertEqual(soup.span.attrs, {})

    def test_m3_attrs_xformer_return(self):
        # Test Case 3: Using attrs_xformer to return a new attribute dict
        html = '<p class="foo" id="bar">Hello</p>'
        
        def replace_attrs(tag):
            # This function *returns* a new dict
            if tag.name == 'p':
                return { "data-new": "true", "processed": "1" }
            return tag.attrs # Must return the original attrs if unchanged
            
        attrs_replacer = SoupReplacer(attrs_xformer=replace_attrs)
        soup = BeautifulSoup(html, "html.parser", replacer=attrs_replacer)
        self.assertEqual(str(soup), '<p data-new="true" processed="1">Hello</p>')

    def test_m3_transformer_combination(self):
        # Test Case 4: Combining name_xformer and xformer
        html = '<b class="bold" id="old">Hello</b><i id="italic">World</i>'
        
        def rename_b(tag):
            return "strong" if tag == "b" else tag
        
        def remove_id(tag):
            # xformer: in-place modification
            if 'id' in tag.attrs:
                del tag.attrs['id']
                
        combo_replacer = SoupReplacer(
            name_xformer=rename_b, 
            xformer=remove_id
        )
        soup = BeautifulSoup(html, "html.parser", replacer=combo_replacer)
        self.assertEqual(str(soup), '<strong class="bold">Hello</strong><i>World</i>')

    def test_m2_compatibility(self):
        # Test Case 5: Test that M2 API still works (part of M3 tests)
        html = "<b>Hello</b>"
        replacer = SoupReplacer("b", "i") # M2-style call
        soup = BeautifulSoup(html, "html.parser", replacer=replacer)
        self.assertEqual(str(soup), "<i>Hello</i>")
        self.assertIsNotNone(soup.i)
        self.assertIsNone(soup.b)

    def test_m3_attrs_xformer_modify_and_return(self):
        # Test Case 6: attrs_xformer modifies and returns existing attrs dict
        html = '<a href="foo.com">link</a><p>text</p>'
        
        def add_target_to_links(tag):
            attrs = tag.attrs # Get current attrs
            if tag.name == 'a' and 'href' in attrs:
                # Modify the dict
                attrs['target'] = '_blank'
            # Return the (possibly modified) dict
            return attrs
        
        replacer = SoupReplacer(attrs_xformer=add_target_to_links)
        soup = BeautifulSoup(html, "html.parser", replacer=replacer)
        self.assertEqual(str(soup), '<a href="foo.com" target="_blank">link</a><p>text</p>')
        



if __name__ == '__main__':
    unittest.main()
