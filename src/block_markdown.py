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
    lines = block.split("\n")

    # Heading check (unchanged, this is usually fine)
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING

    # Code check (Must start AND end with ```)
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE

    # Quote check (EVERY line must start with >)
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE

    # Unordered List check (EVERY line must start with - or *)
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    
    if block.startswith("* "):
        for line in lines:
            if not line.startswith("* "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST

    # Ordered List check (Correct, but ensure it starts at 1)
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST

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
    
    # Using block.lstrip("#").strip() is the safest way to get the clean text
    text = block.lstrip("#").strip()
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)



def quote_to_node(block):
    # 1. Clean the block: remove '>' from each line and strip whitespace
    lines = block.split("\n")
    cleaned_lines = []
    for line in lines:
        if line.strip() == ">": # Handles empty quote lines
            continue
        cleaned_lines.append(line.lstrip(">").strip())
    
    # 2. Join with a single space to avoid double-spacing
    content = " ".join(cleaned_lines)
    
    # 3. Use your text_to_children to handle the bold/italic/etc inside
    children = text_to_children(content)
    
    # 4. Return the ParentNode
    return ParentNode("blockquote", children)

def ul_to_node(block):
    items = []
    for line in block.splitlines():
        item_text = line[2:].strip()
        item_children = text_to_children(item_text)
        
        # FILTER: Only keep children that are NOT None
        valid_children = [child for child in item_children if child is not None]
        
        items.append(ParentNode("li", valid_children))
    return ParentNode("ul", items)


def ol_to_node(block):
    items = []
    for line in block.splitlines():
        parts = line.split(". ", 1)
        if len(parts) == 2 and parts[0].isdigit():
            item_text = parts[1]
        else:
            item_text = parts[1].strip()
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
    # This MUST be two newlines
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block.strip() == "":
            continue
        filtered_blocks.append(block.strip())
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
        return heading_to_html_node(block)
    return paragraph_to_html_node(block)

def extract_title(markdown):
    """Create an extract_title(markdown) function.
It should pull the h1 header from the markdown file (the line that starts with a single #) and return it.
If there is no h1 header, raise an exception.
extract_title("# Hello") should return "Hello" (strip the # and any leading or trailing whitespace)."""

    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block.startswith("# "):
            return block[2:].strip()
    raise Exception("All pages need a h1 header")