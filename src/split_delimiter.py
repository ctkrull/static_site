from textnode import TextNode, TextType

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