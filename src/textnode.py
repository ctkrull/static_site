# We import 'Enum' to create a fixed list of choices. 
# It prevents us from making typos like "bld" instead of "bold".
from enum import Enum

class TextType(Enum):
    # These are the "Types" of text our program can understand.
    # Each name (e.g., BOLD) is linked to a string value ("bold").
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    # The 'Constructor' runs every time you create a new TextNode.
    # It takes the data you provide and "saves" it to the object.
    def __init__(self, text, text_type, url=None):
        self.text = text           # The actual words (e.g., "Click here")
        self.text_type = text_type # The type from the Enum above (e.g., TextType.LINK)
        self.url = url             # Optional: Only used for links or images

    # This is the "Equality" logic. It tells Python HOW to compare two nodes.
    # Without this, Python would only check if they are the exact same spot in memory.
    def __eq__(self, other):
        # We only return 'True' if the text, the type, AND the url match perfectly.
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )
        