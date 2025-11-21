# Milestone-3

## update the implement of the milestone-2 stuff.

Original SoupReplacer:
```python

    class SoupReplacer:
    """
    Specifies a tag replacement to happen during parsing.
    All occurrences of og_tag will be replaced by alt_tag.
    """
    def __init__(self, og_tag, alt_tag):
        self.og_tag = og_tag
        self.alt_tag = alt_tag
    def replace_tag(self, tag_name):
        
        if tag_name == self.og_tag:
            return self.alt_tag
        return tag_name
```

now:

```python


class SoupReplacer:
    """
    SoupReplacer modifies tags during tree construction.

    It can be initialized in two ways:

    1. Milestone 2 API (Simple Replacement):
       replacer = SoupReplacer("original_tag_name", "replacement_tag_name")
       This will just rename all <original> tags to <replacement>.

    2. Milestone 3 API (Transformers):
       replacer = SoupReplacer(name_xformer=fn, attrs_xformer=fn, xformer=fn)
       
       - name_xformer: A function that takes a tag, returns a new tag name (str).
       - attrs_xformer: A function that takes a tag, returns a new attribute dictionary (dict).
       - xformer: A function that takes a tag, modifies it in-place 
                  (e.g., del tag['class']). It returns nothing.
    """
    def __init__(self, *args, name_xformer=None, attrs_xformer=None, xformer=None):
        self.name_xformer = name_xformer
        self.attrs_xformer = attrs_xformer
        self.xformer = xformer
        self.og_tag = none
        self.alt_tag = none
        if args:
            # --- Milestone 2 Logic ---
            if name_xformer or attrs_xformer or xformer:
                raise ValueError(
                    "SoupReplacer cannot mix positional args (M2 API) and keyword args (M3 API)"
                )
            
            if len(args) == 2:
                self.og_tag = og_tag
                self.alt_tag = alt_tag
                
                # Convert M2 logic into an M3 name_xformer
                def m2_name_xformer_impl(tag):
                    if tag.name == self.original_tag:
                        return self.replacement_tag
                    return tag.name
                
                self.name_xformer = m2_name_xformer_impl
            
            elif len(args) > 0:
                raise ValueError(
                    "SoupReplacer positional args must be (original_tag, replacement_tag)"
                )
            # If len(args) == 0, it's the M3 case, do nothing.

    def replace(self, tag):
        """
        Internal method called by the Tag constructor.
        Applies transformers in a specific order:
        1. xformer (general in-place modification)
        2. attrs_xformer (replaces attributes)
        3. name_xformer (replaces name)
        """
        
        # 1. General side-effect transformer
        if self.xformer:
            self.xformer(tag)
        
        # 2. Attribute transformer (must return a new dict)
        if self.attrs_xformer:
            new_attrs = self.attrs_xformer(tag)
            if not isinstance(new_attrs, dict):
                raise TypeError(
                    f"attrs_xformer must return a dict, but it returned {type(new_attrs)}"
                )
            tag.attrs = new_attrs

        # 3. Name transformer (must return a new string)
        if self.name_xformer:
            new_name = self.name_xformer(tag)
            if not isinstance(new_name, str):
                raise TypeError(
                    f"name_xformer must return a str, but it returned {type(new_name)}"
                )
            tag.name = new_name
```


then update TreeBuilder class and Tag class to initiate the replacer.

## Test:
test is in bs4\tests\test_soup_replacer.py
task7.py in Apps\m3

usage of task7:
```bash
    .\venv\Scripts\Activate.ps1
    cd Apps
    cd m3
    python task7.py test.html


```

usage of test
```bash
    cd bs4
    cd tests
    python test_soup_replacer.py
```

## Technical Report:

### Milestone 2

#### Pros:

1.Simple and intuitive API for tag replacement.

2.Easy to understand and implement.

#### Cons:

1.Limited to tag name replacement.

2.Cannot manipulate attributes or perform conditional transformations.

### Milestone 3

#### Pros:

1.Provides full flexibility at the node and attribute level.

2.Supports multiple types of transformations (tag name, attributes, in-place side effects).

#### Cons:

1.Slightly more complex API; requires user to understand lambdas/functions.

2.Users must be aware that name_xformer receives strings, while attrs_xformer and xformer receive Tag objects.

### Potential Future Enhancements

1.Selector-based transformations

Allow users to provide CSS selectors or XPath-like queries to target nodes.

This would reduce the need for conditional logic in lambda functions.

2.Chaining transformations

Enable multiple SoupReplacer instances to be combined or chained for batch processing.

3.Logging / Debugging support

Optional logging of transformations could help users verify replacements during parsing.

4.Performance optimization

If applied to large HTML/XML documents, repeated function calls for every node could be optimized.

Consider caching common transformations or supporting batch operations.

### Conclusion

Milestone 3 significantly extends SoupReplacer from a simple tag replacement utility to a powerful, node-level transformation tool. The new API balances flexibility with usability, enabling complex HTML modifications during parsing while maintaining backward compatibility with Milestone 2. Future enhancements could further improve usability, performance, and debugging capabilities.