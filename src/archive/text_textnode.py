from textnode import TextNode, TextType, text_node_to_html_node
from inline_markdown import split_nodes_delimiter, text_to_textnodes, split_nodes_image, split_nodes_link, extract_markdown_images, extract_markdown_links


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
   