class HTMLNode:
    # We set everything to 'None' by default so we can create
    # a node even if we don't have all the info yet.
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag           # The HTML tag, like "p" or "a"
        self.value = value       # The text inside the tag
        self.children = children # A list of other HTMLNode objects inside this one
        self.props = props       # A dictionary of attributes like {"href": "url"}

    def to_html(self):
        # We haven't built this yet! This is a "placeholder" that
        # reminds us (or other devs) that child classes MUST define this.
        raise NotImplementedError("child classes must implement to_html method")

    def props_to_html(self):
        # If there are no attributes, we return an empty string
        # so we don't try to loop through 'None' and crash.
        if self.props is None:
            return ""
        
        # This is where we "Translate" the Dictionary into a String.
        props_html = ""
        for key, value in self.props.items():
            # We add a leading space and the key="value" format.
            # Example: {"href": "google.com"} becomes ' href="google.com"'
            props_html += f' {key}="{value}"'
        return props_html

    def __repr__(self):
        # This is purely for YOU. When you print(node), this shows
        # you exactly what's inside so you don't have to guess.
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"


# Child Class inherits from Parent
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        # This is perfect. You're telling the parent 'HTMLNode' 
        # that a LeafNode always has 'None' for children.
        super().__init__(tag, value, None, props)

    def to_html(self):
        # 1. This is correct! We can't have an empty leaf.
        if self.value is None:
            raise ValueError("Invalid HTML: no value")
        
        # 2. This is also correct! If there's no tag, it's just raw text.
        if self.tag is None:
            return self.value
        
        # 3. HERE is the fix: 
        # We need to return a string that looks like HTML: <tag props>value</tag>
        # We use your props_to_html() method from the parent class here.
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        # The assignment asks for this to be similar to HTMLNode 
        # but specifically without the "children" part.
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


