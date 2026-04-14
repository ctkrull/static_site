from htmlnode import ParentNode, LeafNode  # To build the HTML objects
from textnode import TextNode, TextType    # To handle the text inside blocks
from inline_markdown import text_to_textnodes # To break down bold/italic/links/images
from block_markdown import markdown_to_blocks, block_to_html_node
from text_to_children import text_to_children


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


def markdown_to_html_node(markdown_text):
    return markdown_text_to_html_node(markdown_text)