import sys
import os

# --- Setup to import Mock Classes from the test file ---
# We assume the mock classes for testing (MockBeautifulSoup, MockTag, MockString) 
# are defined in the unit tests file, which correctly inherits NavigableElement.
try:
    # Adjust path to find the test file relative to the current script location
    script_dir = os.path.dirname(__file__)
    # Path to bs4/tests/m4_unit_tests.py
    test_path = os.path.join(script_dir, "../../bs4/tests")
    if test_path not in sys.path:
        sys.path.insert(0, test_path)

    # Import the necessary Mock classes for demonstration
    from m4_unit_tests import MockBeautifulSoup, MockTag, MockString
    
except ImportError:
    print("Error: Could not import Mock classes from m4_unit_tests.py.")
    print("Please ensure 'm4_unit_tests.py' is correctly placed in 'bs4/tests/' directory.")
    sys.exit(1)


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

def run_m4_test():
    """Executes the M4 iteration test and prints the results."""
    
    # 1. Create the tree structure
    soup_instance = create_sample_tree()
    
    print("--- M4 Iteration Feature Demonstration ---")
    print("Traversal Mode: Depth-First Search (DFS)")
    print("Starting Node: MockBeautifulSoup (Entire Document)")
    print("-" * 30)
    
    # 2. Use the M4 implemented __iter__ for iteration
    
    print("Traversal Results:")
    node_count = 0
    
    for node in soup_instance:
        node_count += 1
        
        # Identify node type and print
        if isinstance(node, MockBeautifulSoup):
            print(f"[{node_count:02}] (Root) {node.name}")
        elif isinstance(node, MockTag):
            # Tag node (recursion handled by __iter__ internally)
            print(f"[{node_count:02}] <Tag>   <{node.name}>")
        elif isinstance(node, MockString):
            # NavigableString node
            print(f"[{node_count:02}] Text    '{node.text}'")
        else:
            print(f"[{node_count:02}] Unknown Type: {type(node)}")
            
    print("-" * 30)
    print(f"Total nodes traversed: {node_count}.")
    print("If the output order is: Doc, A, B, Text1, C, D, the iteration feature is working correctly.")


if __name__ == "__main__":
    run_m4_test()