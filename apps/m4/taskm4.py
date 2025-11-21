import sys
import os
import time

# Assuming the modified bs4 library is accessible in the Python path
try:
    from bs4 import BeautifulSoup, Tag, NavigableString
except ImportError:
    print("Error: Could not import BeautifulSoup, Tag, or NavigableString.")
    print("Please ensure your modified bs4 package is correctly installed or accessible.")
    sys.exit(1)


def run_m4_demo(file_path: str):
    """
    Parses an HTML file, demonstrates the M4 iteration feature,
    measures traversal time, and saves the output to a file.
    """
    try:
        # 1. Read the input HTML file
        with open(file_path, 'r', encoding='utf-8') as f:
            markup = f.read()

        # 2. Create the BeautifulSoup object
        # Note: This is where the M4 __iter__ logic is applied to the soup object
        start_parse = time.time()
        soup = BeautifulSoup(markup, "html.parser")
        end_parse = time.time()

        output_lines = []
        output_lines.append(f"--- M4 Document Traversal Demo ---")
        output_lines.append(f"Input file: {file_path}")
        output_lines.append(f"Time taken for parsing: {end_parse - start_parse:.6f} seconds")
        output_lines.append("Starting Depth-First Iteration over the soup object...")
        output_lines.append("-" * 40)

        
        # --- 3. M4 Traversal (Lazy/Streaming) and Output Collection ---
        start_m4_traversal = time.time()
        node_count = 0
        
        # This loop uses the generator (__iter__) implemented in M4
        for node in soup:
            
            # Identify and print node information (collecting into list)
            line = ""
            if isinstance(node, BeautifulSoup):
                line = f"[{node_count+1:03}] TYPE: Document (Root)"
            elif isinstance(node, Tag):
                line = f"[{node_count+1:03}] TYPE: Tag, Name: <{node.name}>"
            elif isinstance(node, NavigableString):
                # Text, comments, or other navigable strings
                text_preview = node.strip()
                if text_preview:
                    # Replace newlines in the preview for cleaner output file
                    line = f"[{node_count+1:03}] TYPE: String, Content: '{text_preview[:40].replace('\n', ' ')}...'"
                else:
                    # Skip empty whitespace strings for cleaner output
                    continue
            else:
                # Other types of nodes (e.g., Declaration, Doctype)
                line = f"[{node_count+1:03}] TYPE: Other Node ({type(node).__name__})"
            
            output_lines.append(line)
            node_count += 1 # Only count non-skipped nodes

        end_m4_traversal = time.time()
        m4_time = end_m4_traversal - start_m4_traversal
        
        output_lines.append("-" * 40)
        output_lines.append(f"Traversal complete. Total non-whitespace nodes visited: {node_count}.")


        # --- 4. Performance Comparison (Eager Loading) ---
        start_eager_load = time.time()
        # Forcing the generator to yield ALL nodes and collect them into a list 
        # (Simulating the older, non-streaming approach M4 avoids)
        all_nodes_list = list(soup) 
        end_eager_load = time.time()
        eager_time = end_eager_load - start_eager_load
        
        # 5. Output Results and Timing Comparison
        
        comparison_lines = []
        comparison_lines.append("\n--- Performance Comparison (M4 Lazy vs. Eager Loading) ---")
        comparison_lines.append(f"1. M4 Streaming Traversal Time (Lazy): {m4_time:.6f} seconds (Time taken while processing/printing)")
        comparison_lines.append(f"2. List Collection Traversal Time (Eager): {eager_time:.6f} seconds (Time taken to collect all {len(all_nodes_list)} nodes into a list)")
        comparison_lines.append(f"Note: M4's lazy generator is most efficient when you process a large document and break the loop early.")
        comparison_lines.append("-" * 60)
        
        
        # --- 6. Save Traversal Output to File ---
        output_filename = "m4_traversal_output.txt"
        
        # Combine traversal output and comparison lines
        final_output = "\n".join(output_lines) + "\n" + "\n".join(comparison_lines)
        
        with open(output_filename, 'w', encoding='utf-8') as outfile:
            outfile.write(final_output)

        # 7. Print summary to console
        print(final_output)
        print(f"\nTraversal log successfully saved to: {output_filename}")


    except FileNotFoundError:
        print(f"Error: Input file not found at path: {file_path}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python task_m4_demo.py <path_to_html_file>")
        sys.exit(1)

    # Get the file path from the command line argument
    input_file_path = sys.argv[1]
    run_m4_demo(input_file_path)