import re
from textnode import TextNode, TextType, text_node_to_html_node


def split_nodes_image(old_nodes):
    pattern = re.compile(r"!\[([^\]]*)\]\(([^\)]*)\)")
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        last_index = 0
        for match in pattern.finditer(text):
            if match.start() > last_index:
                new_nodes.append(TextNode(text[last_index:match.start()], TextType.TEXT))

            alt_text = match.group(1)
            url = match.group(2)
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url=url))
            last_index = match.end()

        if last_index < len(text):
            new_nodes.append(TextNode(text[last_index:], TextType.TEXT))
        elif last_index == 0:
            new_nodes.append(node)

    return new_nodes


def split_nodes_link(old_nodes):
    pattern = re.compile(r"(?<!!)\[([^\]]*)\]\(([^\)]*)\)")
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        last_index = 0
        for match in pattern.finditer(text):
            if match.start() > last_index:
                new_nodes.append(TextNode(text[last_index:match.start()], TextType.TEXT))

            link_text = match.group(1)
            url = match.group(2)
            new_nodes.append(TextNode(link_text, TextType.LINK, url=url))
            last_index = match.end()

        if last_index < len(text):
            new_nodes.append(TextNode(text[last_index:], TextType.TEXT))
        elif last_index == 0:
            new_nodes.append(node)

    return new_nodes

def extract_markdown_images(text):
    # This regex looks for the Markdown image syntax: ![alt text](url)
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)

    # Each match is a tuple (alt_text, url)
    return matches

def extract_markdown_links(text):
    # This regex looks for the Markdown link syntax: [link text](url)
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    
    # Each match is a tuple (link_text, url)
    links = []
    for link_text, url in matches:
        links.append({'text': link_text, 'url': url})
    
    return links


def text_to_textnodes(text):
    """Convert plain text into a list of TextNode objects.

    The function uses the existing helpers in this order:
    1) split inline code with `split_nodes_delimiter(..., "`", TextType.CODE)`
    2) split bold text with `split_nodes_delimiter(..., "**", TextType.BOLD)`
    3) split italic text with `split_nodes_delimiter(..., "*", TextType.ITALIC)`
    4) turn image markdown into IMAGE nodes with `split_nodes_image`
    5) turn link markdown into LINK nodes with `split_nodes_link`
    """

    nodes = [TextNode(text, TextType.TEXT)]

    # 1) Parse inline code first so backticks are preserved inside code.
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

    # 2) Parse bold text before italic text.
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)

    # 3) Parse markdown images and links from remaining plain TEXT nodes.
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        # Rule: We ONLY split nodes that are plain text. 
        # If it's already Bold or Italic, we leave it alone.
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
            
        # Split the text by the delimiter (e.g., "**" or "`")
        parts = old_node.text.split(delimiter)
        
        # If we split and get an even number of parts (0, 2, 4...),
        # it means a closing delimiter is missing! (e.g., "This `code is broken")
        if len(parts) % 2 == 0:
            raise ValueError("Invalid markdown, terminated block not found")
        
        # Now we loop through our parts and turn them into TextNodes
        for i in range(len(parts)):
            if parts[i] == "":
                continue
            if i % 2 == 0:
                # Even index (0, 2, 4) = Outside the delimiters
                new_nodes.append(TextNode(parts[i], TextType.TEXT))
            else:
                # Odd index (1, 3, 5) = Inside the delimiters
                new_nodes.append(TextNode(parts[i], text_type))
    
    return new_nodes
   