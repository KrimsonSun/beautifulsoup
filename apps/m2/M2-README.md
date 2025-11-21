# Milestone-2
### Part 1. Remake of the task2,3,4 by using SoupStrainer.
#### task usage:

```bash
    python taskx.py your/path/name
```
#### x is the task number you want to test.


### Part 2. Locate used APIs.

#### here is the list of the used APIs and the line number.

| API/Concept | Actual Function/Attribute | File Name | Line Number (in provided file) |
| :--- | :--- | :--- | :--- |
| **Parser Initialization** | `TreeBuilder.__init__` | `__init__.py` | L213 |
| **Attribute Processing** | `TreeBuilder._replace_cdata_list_attribute_values` | `__init__.py` | L358 |
| **HTML Attribute List** | `HTMLTreeBuilder.DEFAULT_CDATA_LIST_ATTRIBUTES` | `__init__.py` | L527 |
| **Parsing Entry Point** | `TreeBuilder.feed` | `__init__.py` | L315 |

for bs4/init.py

on line L133

create class SoupReplacer:

```python
    class SoupReplacer:
    """
    Specifies a tag replacement to happen during parsing.
    All occurrences of og_tag will be replaced by alt_tag.
    """
    def __init__(self, og_tag, alt_tag):
        # The tag name to be replaced (e.g., "b")
        self.og_tag = og_tag
        # The tag name to replace it with (e.g., "blockquote")
        self.alt_tag = alt_tag
```
on line L284

update the constructor,add the initialization method of the :
```python

    ##----the replacer workflow---
        self.replacer = kwargs.pop('replacer', None)
        if self.replacer and not isinstance(self.replacer, SoupReplacer):
            # You might need to import SoupReplacer here if it's in a separate file
            raise ValueError("The 'replacer' argument must be a SoupReplacer instance.")
    ##---END----
```

for file bs4/builder/init.py

on L182
```python

    # --- New Code for SoupReplacer Execution ---
    # Access the replacer object stored on the BeautifulSoup instance
    replacer = self.soup.replacer
    
    # Check if replacement is enabled and matches the current tag name
    if replacer and replacer.og_tag == name:
        name = replacer.alt_tag # Replace the tag name before object creation
    # --- End New Code ---
```
task6 usage:
```bash
    cd apps\m2
    python task6.py your_file_path
 ```   
To do the test on the large fileL: I choose a xml file with many comments, the file is 1.9GB

```bash
    .\venv\Scripts\Activate.ps1 
    pytest bs4/tests/test_xml_replacer.py
```


# IMPORTANT UPDATE
I change the task6 replacer test object, because I update the SoupReplacer in Milestone3 ,
and I add a test.html without <b> tag ,now the test file will turn a b tag to h2 tag.