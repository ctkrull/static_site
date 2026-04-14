from enum import Enum

class BlockType(Enum):
    # These are the "Types" of blocks our program can understand.
    # Each name (e.g., PARAGRAPH) is linked to a string value ("paragraph").
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote" 
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    # This function takes a block of text and determines its type based on markdown syntax.
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    elif block.startswith("```"):
        return BlockType.CODE
    elif block.startswith("> "):
        return BlockType.QUOTE
    elif block.startswith("- "):
        return BlockType.UNORDERED_LIST
    elif block[0].isdigit() and block[1:3] == ". ":
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH

def markdown_to_blocks(markdown):
    """Convert markdown text into a list of Block objects.

    The function should:
    1) Split the text into paragraphs by newlines.

    """


    blocks = markdown.split('\n\n')
    filtered_blocks = []
    
    for block in blocks:
        block = block.strip()
        if block != "":
            filtered_blocks.append(block)


    return filtered_blocks