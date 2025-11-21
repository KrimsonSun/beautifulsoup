# Milestone-4
## Iterable Beautiful Soup (__iter__)

### Core Objective

To enable direct iteration over the BeautifulSoup object, supporting the standard Python loop
```python
 for node in soup:
```

### Technical Implementation

Method: Implement the special method __iter__ on the core base class NavigableElement.

Algorithm: Utilizes a non-recursive Depth-First Search (DFS), managing the traversal state with an explicit stack.

### Key Features (Performance)
1. Streaming Output (Lazy): Uses the yield keyword as a Generator to output nodes one by one.

2. Memory Efficiency: Strictly adheres to the constraint of not pre-collecting all nodes into a list, making it suitable for processing large HTML documents.

3. Traversal Order: Ensures nodes are visited in document order (top-to-bottom, depth-first).



### Implementation Code

The core logic for iteration is implemented in the __iter__ method of the NavigableElement base class.



```python 
class NavigableElement:
    # This class mocks the base element that BeautifulSoup and Tag inherit from.
    
    def __init__(self, name=None, contents=None):
        self.name = name
        # contents holds the list of child nodes
        self.contents = contents if contents is not None else []
        
    def __iter__(self):
        """
        Non-recursive generator for depth-first traversal in document order.
        """
        # 1. Yield the starting node (root/tag) itself
        yield self 

        # 2. Use a stack for non-recursive DFS
        stack = []
        
        # 3. Initialize stack with children in reverse order
        # LIFO stack pops them in document order (left-to-right)
        if self.contents:
            stack.extend(reversed(self.contents))

        while stack:
            node = stack.pop()
            
            # 4. Yield the current node
            yield node
            
            # 5. Push children onto the stack (maintaining DFS order)
            if hasattr(node, 'contents') and node.contents:
                stack.extend(reversed(node.contents))

```


### Demonstration Script (beautifulsoup/apps/m4/task_m4_demo.py)

This script is designed to demonstrate the M4 feature on an actual HTML file and compare its performance against the non-streaming approach.

##### Script Functionality

1. Input: Reads an HTML file path provided as a command-line argument.

2. Traversal: Performs a full Depth-First Traversal using the implemented for node in soup: mechanism.

3. Performance Test: Compares the time taken for the M4 Lazy Streaming Traversal vs. the time taken for Eager Loading (i.e., list(soup), which forces the collection of all nodes).

4. Output: Prints the timing summary to the console and saves a detailed log of the traversal order and performance data to a file.

#### Usage and Output

1. Usage
```bash
python task_m4_demo.py <path_to_html_file>
```
2. Console Output:

A summary of the parsing time and a comparison of the Lazy vs. Eager traversal times.

3. File Output

A file named m4_traversal_output.txt containing the ordered list of every visited node and the final performance comparison.

#### Unit Tests (bs4/tests/m4_unit_tests.py)

This file contains formal unit tests using the Python unittest framework to verify the correctness and order of the M4 iteration feature.

Usage :
```python
cd bs4\tests

python test_m4_DFS_iteration.py
```


##### Purpose

The tests ensure that the NavigableElement.__iter__ generator consistently produces nodes in the correct Depth-First Search (DFS) document order under various tree structures.

Test Coverage Highlights

Mocking: Uses MockBeautifulSoup, MockTag, and MockString classes which inherit NavigableElement to simulate the tree structure and iteration logic.

1. test_1_simple_flat_tree_iteration: Verifies iteration over a root node with immediate children.

2. test_2_nested_tree_depth_first_traversal: Confirms the primary DFS behavior for nested tags (e.g., A before its siblings, B before its siblings).

3. test_3_mixed_content_with_navigable_strings: Ensures strings (text nodes) are correctly included in the traversal order alongside tags.

4. test_5_wide_and_deep_tree_iteration_order: Comprehensive test to validate order across complex, non-trivial document structures.