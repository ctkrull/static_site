import re
from textnode import TextNode, TextType


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