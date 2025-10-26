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

### Part 3. Re