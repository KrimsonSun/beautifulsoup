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

        if args:
            # --- Milestone 2 Logic ---
            if name_xformer or attrs_xformer or xformer:
                raise ValueError(
                    "SoupReplacer cannot mix positional args (M2 API) and keyword args (M3 API)"
                )
            
            if len(args) == 2:
                self.original_tag = args[0]
                self.replacement_tag = args[1]
                
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

