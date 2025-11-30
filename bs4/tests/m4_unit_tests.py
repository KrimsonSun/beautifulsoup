import sys
import os
import unittest # <-- Added for formal testing

# --- Setup to import Mock Classes from the test file ---
# We assume the mock classes for testing (MockBeautifulSoup, MockTag, MockString) 
# are defined in the unit tests file, which correctly inherits NavigableElement.
try:
    # Adjust path to find the test file relative to the current script location
    script_dir = os.path.dirname(__file__)
    # Path to bs4/tests/m4_unit_tests.py
    # NOTE: Using relative import 'from .m4_unit_tests' is often cleaner
    # but maintaining the original path manipulation for compatibility.
    test_path = os.path.join(script_dir, "../../bs4/tests")
    if test_path not in sys.path:
        sys.path.insert(0, test_path)

    # Import the necessary Mock classes for demonstration
    from m4_unit_tests import MockBeautifulSoup, MockTag, MockString, MockComment # Assuming MockComment exists
    
except ImportError:
    print("Error: Could not import Mock classes from m4_unit_tests.py.")
    print("Please ensure 'm4_unit_tests.py' is correctly placed in 'bs4/tests/' directory.")
    sys.exit(1)


# --- Helper Function to Create the Sample Tree (Kept as-is) ---
def create_sample_tree():
    """
    Creates and returns a mock HTML tree for iteration testing.
    Structure: Doc -> A -> B (Text1, C), Doc -> D
    Expected DFS traversal order: Doc, A, B, Text1, C, D
    """
    
    # Text node inside B
    text_1 = MockString("Section Text")
    
    # C node (child of B)
    tag_c = MockTag('c')
    
    # B node (child of A), containing text_1 and C
    tag_b = MockTag('b', contents=[text_1, tag_c])
    
    # A node (root child), containing B
    tag_a = MockTag('a', contents=[tag_b])
    
    # D node (another root child)
    tag_d = MockTag('d')
    
    # Document Root (MockBeautifulSoup)
    doc = MockBeautifulSoup(contents=[tag_a, tag_d])
    
    return doc

# --- Helper to Extract Node Names for Assertions ---
def get_node_names(node_sequence):
    """Extracts node identifiers (name or string content) for assertion."""
    names = []
    for node in node_sequence:
        if isinstance(node, MockBeautifulSoup):
            names.append(node.name) # Typically 'doc' or similar
        elif isinstance(node, MockTag):
            names.append(node.name)
        elif isinstance(node, MockString):
            # For simplicity in assertions, use the string content
            names.append(str(node)) 
        else:
            names.append(f"<{type(node).__name__}>") # For other types like Comment
    return names

# ======================================================================
#                            FORMAL UNIT TESTS
# ======================================================================

class TestBeautifulSoupIteration(unittest.TestCase):
    
    ## Test 1: Nested Structure (Original Demo converted to Test)
    def test_1_nested_tree_traversal(self):
        """
        Tests the core DFS traversal order on a nested tree structure 
        starting from the root (MockBeautifulSoup).
        """
        soup_instance = create_sample_tree()
        
        # Expected DFS order: Doc, A, B, Text1, C, D
        expected = ['doc', 'a', 'b', 'Section Text', 'c', 'd']
        
        # Get actual order using the implemented __iter__
        actual = get_node_names(soup_instance)
        
        self.assertEqual(actual, expected, "Test 1: Core nested DFS failed.")

    ## Test 2: Flat Structure and Boundary Condition (Empty Document)
    def test_2_empty_document_traversal(self):
        """
        Tests iteration on an empty document (boundary condition).
        Should only yield the root node itself.
        """
        # doc -> []
        doc = MockBeautifulSoup(name='doc', contents=[])
        
        # Expected DFS order: doc
        expected = ['doc']
        
        actual = get_node_names(doc)
        
        self.assertEqual(actual, expected, "Test 2: Empty document failed.")
        self.assertEqual(len(actual), 1, "Test 2: Empty document should only yield 1 node.")
        
    ## Test 3: Starting Iteration from a Tag (Non-Root)
    def test_3_start_from_intermediate_tag(self):
        """
        Tests iteration starting from an intermediate Tag (non-root) node.
        Should start by yielding the tag itself.
        """
        # A -> [ B -> ['Text'], C ]
        tag_b = MockTag('b', contents=[MockString('Text')])
        tag_c = MockTag('c')
        tag_a = MockTag('a', contents=[tag_b, tag_c])
        
        # Expected DFS order starting from 'a': A, B, Text, C
        expected = ['a', 'b', 'Text', 'c']
        
        actual = get_node_names(tag_a)
        
        self.assertEqual(actual, expected, "Test 3: Iteration from non-root tag failed.")

    ## Test 4: Traversal with Special NavigableString Subclasses (e.g., Comment)
    def test_4_traversal_with_special_elements(self):
        """
        Tests if special NavigableString subclasses (like Comment) are correctly yielded 
        and traversed in DFS order. (Requires MockComment to exist)
        """
        # D -> [ C, ]
        tag_c = MockTag('c')
        # Assuming MockComment is a subclass of MockString/NavigableElement
        comment = MockComment("A hidden note") 
        
        tag_d = MockTag('d', contents=[tag_c, comment])
        
        # Expected DFS order: D, C, A hidden note (using string content for assertion)
        expected = ['d', 'c', 'A hidden note'] 
        
        actual = get_node_names(tag_d)
        
        self.assertEqual(actual, expected, "Test 4: Traversal with Comment node failed.")

    ## Test 5: Traversal of a Wide Tree (Ensuring LIFO Stack Order)
    def test_5_wide_structure_order(self):
        """
        Tests a wide, flat structure to ensure the non-recursive stack correctly 
        maintains the left-to-right (document) order.
        """
        # doc -> [ A, B, C ]
        structure = {
            'name': 'doc',
            'contents': [{'name': 'A'}, {'name': 'B'}, {'name': 'C'}]
        }
        doc = MockBeautifulSoup(name='doc', contents=[
            MockTag('A'), 
            MockTag('B'), 
            MockTag('C')
        ])
        
        # Expected DFS order (simple L-to-R): doc, A, B, C
        expected = ['doc', 'A', 'B', 'C']
        
        actual = get_node_names(doc)
        
        self.assertEqual(actual, expected, "Test 5: Wide structure LIFO order failed.")


# --- Execution (Replaced the original run_m4_test with unittest runner) ---
if __name__ == "__main__":
    # If this script is run directly, execute the unit tests
    unittest.main()