import re

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