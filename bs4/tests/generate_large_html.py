# generate_large_html.py

import os
import time
import sys

# Set the target file size to 1 GB (1024 * 1024 * 1024 bytes)
TARGET_SIZE_GB = 1
TARGET_SIZE_BYTES = TARGET_SIZE_GB * 1024 * 1024 * 1024
# This file name must match the one used in 'test_performance_html.py'
OUTPUT_FILENAME = "large_test_document_html.html" 

# HTML chunk template containing the target tag (<b>) for replacement
template_chunk = """
<div class="test-block" data-index="{}">
    <h3>Data Record {}</h3>
    <p>This paragraph contains the replacement target.</p>
    <p>The target tag is <b>bold item {}</b>, which will be replaced by the SoupReplacer.</p>
    <a href="#link-{}">Link</a>
</div>
"""

current_size = 0
chunk_count = 0

print(f"Generating file: {OUTPUT_FILENAME} (Target size: {TARGET_SIZE_GB} GB)")

start_time = time.time()

try:
    with open(OUTPUT_FILENAME, 'w', encoding='utf-8') as f:
        # Write HTML header
        f.write("<!DOCTYPE html><html><head><title>Large Performance Test File</title></head><body>\n")
        
        while current_size < TARGET_SIZE_BYTES:
            chunk_count += 1
            # Format the chunk with unique IDs/values
            content = template_chunk.format(chunk_count, chunk_count, chunk_count, chunk_count)
            f.write(content)
            # Use encoding size for accurate byte count
            current_size += len(content.encode('utf-8')) 
            
            if chunk_count % 50000 == 0:
                print(f"   Wrote {chunk_count} blocks. Current size: {current_size / (1024*1024):.2f} MB")
        
        # Write HTML footer
        f.write("\n</body></html>")
        
except Exception as e:
    print(f"An error occurred during file generation: {e}")
    sys.exit(1)

end_time = time.time()

final_size_gb = current_size / (1024 * 1024 * 1024)
print("\n--- Generation Complete ---")
print(f"Final size of {OUTPUT_FILENAME}: {final_size_gb:.3f} GB")
print(f"Total chunks generated: {chunk_count}")
print(f"Time taken: {end_time - start_time:.2f} seconds")