import time
import sys

# Assume the modified bs4 library is accessible in the Python path
# Ensure both BeautifulSoup and SoupReplacer can be imported from your modified library
try:
    from bs4 import BeautifulSoup, SoupReplacer
except ImportError:
    print("Error: Could not import BeautifulSoup or SoupReplacer.")
    print("Please ensure your modified bs4 package is correctly installed or accessible.")
    sys.exit(1)


def run_task6(file_path: str):
    """
    Parses a file using the SoupReplacer API, measures performance,
    and saves the output.
    """

    # 1. Define the replacement rule: 'b' tag -> 'blockquote' tag
    REPLACER = SoupReplacer("b", "blockquote")

    try:
        # Read the large markup file
        with open(file_path, 'r', encoding='utf-8') as f:
            markup = f.read()

        # --- Performance Measurement: Start ---
        start_time = time.time()

        # 2. Use the new API for parsing and replacement
        # The replacement happens internally as the parser builds the tree.
        soup = BeautifulSoup(markup, "html.parser", replacer=REPLACER)

        # --- Performance Measurement: End ---
        end_time = time.time()

        # 3. Save the modified tree
        output_filename = "task6_replacement_output.html"
        with open(output_filename, 'w', encoding='utf-8') as outfile:
            outfile.write(soup.prettify())

        # 4. Output results
        print(f"--- Task 6: SoupReplacer Execution Summary ---")
        print(f"Input file: {file_path}")
        print(f"Output file: {output_filename}")
        print(f"Replacement Rule: '{REPLACER.og_tag}' -> '{REPLACER.alt_tag}'")
        print(f"Time taken for parsing and replacement: {end_time - start_time:.4f} seconds")

        # 5. Verification Check (Simple check, not exhaustive)
        if soup.find('b') is None and soup.find('blockquote') is not None:
            print("Verification: SUCCESS - Original 'b' tags are gone, 'blockquote' tags found.")
        else:
            print("Verification: WARNING - Replacement check failed (check output file manually).")

    except FileNotFoundError:
        print(f"Error: Input file not found at path: {file_path}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python task6.py <path_to_large_html_file>")
        sys.exit(1)

    # Get the file path from the command line argument
    input_file_path = sys.argv[1]
    run_task6(input_file_path)