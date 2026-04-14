from htmlnode import HTMLNode, LeafNode

def text_to_children(text):
    # 1. Convert the raw string into a list of TextNodes 
    # (You've likely already built functions like 'text_to_textnodes' for this)
    text_nodes = text_to_textnodes(text)
    
    children = []
    for text_node in text_nodes:
        # 2. Convert each TextNode into an HTMLNode (LeafNode)
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    
    return children