from enum import Enum
from htmlnode import ParentNode, LeafNode  # To build the HTML objects
from textnode import TextNode, TextType    # To handle the text inside blocks
from inline_markdown import text_to_textnodes # To break down bold/italic/links/images
from text_to_children import text_to_children

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
    elif block.startswith(("- ", "* ")):
        return BlockType.UNORDERED_LIST
    elif block[0].isdigit() and block[1:3] == ". ":
        lines = block.splitlines()
        expected = 1
        for line in lines:
            if line.startswith(f"{expected}. "):
                expected += 1
            else:
                return BlockType.PARAGRAPH
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH


def markdown_text_to_html_node(markdown_text):
    # This function takes a markdown document into a single parent(HTMLNode)
    markdown_blocks = markdown_to_blocks(markdown_text)
    children = []
    for block in markdown_blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children)

def paragraph_to_html_node(block):
    # Join lines if it's a multi-line paragraph
    lines = block.split("\n")
    paragraph_text = " ".join(lines)
    # Get the children (bold, italic, etc)
    children = text_to_children(paragraph_text)
    return ParentNode("p", children)

def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    # Get text after the hashes and the space
    text = block[level + 1:]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

# Aliases for the block_to_html_node helper names used in tests.
paragraph_to_node = paragraph_to_html_node
heading_to_node = heading_to_html_node


def quote_to_node(block):
    lines = [line[2:] if line.startswith("> ") else line for line in block.splitlines()]
    quote_text = "\n".join(lines)
    children = text_to_children(quote_text)
    return ParentNode("blockquote", children)


def ul_to_node(block):
    items = []
    for line in block.splitlines():
        if line.startswith("- ") or line.startswith("* "):
            item_text = line[2:]
        else:
            item_text = line
        item_children = text_to_children(item_text)
        items.append(ParentNode("li", item_children))
    return ParentNode("ul", items)


def ol_to_node(block):
    items = []
    for line in block.splitlines():
        parts = line.split(". ", 1)
        if len(parts) == 2 and parts[0].isdigit():
            item_text = parts[1]
        else:
            item_text = line
        item_children = text_to_children(item_text)
        items.append(ParentNode("li", item_children))
    return ParentNode("ol", items)


def code_to_node(block):
    start = block.find("```") + 3
    end = block.rfind("```")
    code_text = block[start:end]
    if code_text.startswith("\n"):
        code_text = code_text[1:]
    return ParentNode("pre", [ParentNode("code", [LeafNode(None, code_text)])])


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

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.QUOTE:
        return quote_to_node(block)
    if block_type == BlockType.UNORDERED_LIST:
        return ul_to_node(block)
    if block_type == BlockType.ORDERED_LIST:
        return ol_to_node(block)
    if block_type == BlockType.CODE:
        return code_to_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_node(block)
    return paragraph_to_node(block)