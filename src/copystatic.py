import shutil
import os
from markdown_html import markdown_to_html_node
from block_markdown import extract_title

def copy_static_recursive(source, dest):
    # 1. If the destination doesn't exist, create it
    if not os.path.exists(dest):
        os.mkdir(dest)

    # 2. List everything in the current source folder
    for item in os.listdir(source):
        from_path = os.path.join(source, item)
        to_path = os.path.join(dest, item)
        
        print(f" * {from_path} -> {to_path}") # Logging is recommended!

        if os.path.isfile(from_path):
            # Base case: it's a file, so just copy it
            shutil.copy(from_path, to_path)
        else:
            # Recursive step: it's a directory, so call THIS function again
            copy_static_recursive(from_path, to_path)



def generate_page(from_path, template_path, dest_path, basepath="/"):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    with open(from_path, "r") as f:
        markdown_content = f.read()
    with open(template_path, "r") as f:
        template = f.read()

    node = markdown_to_html_node(markdown_content)
    html_content = "".join([child.to_html() for child in node.children])
    title = extract_title(markdown_content)

    # STEP 1: Insert your content into the template placeholders
    # This is what fixes the "{{ Content }}" issue in your screenshot!
    full_html = template.replace("{{ Title }}", title)
    full_html = full_html.replace("{{ Content }}", html_content)

    # STEP 2: Handle the basepath for GitHub Pages
    full_html = full_html.replace('href="/', f'href="{basepath}')
    full_html = full_html.replace('src="/', f'src="{basepath}')

    dest_dir = os.path.dirname(dest_path)
    if dest_dir != "":
        os.makedirs(dest_dir, exist_ok=True)
    
    with open(dest_path, "w") as f:
        f.write(full_html)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath="/"):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)

        if os.path.isfile(from_path):
            if filename.endswith(".md"):
                # Ensure the destination is an .html file
                dest_file_path = dest_path.replace(".md", ".html")
                generate_page(from_path, template_path, dest_file_path, basepath)
        else:
            # It's a directory! 
            # 1. Create the directory in 'public' so the files have a home
            os.makedirs(dest_path, exist_ok=True)
            # 2. Recurse into it
            generate_pages_recursive(from_path, template_path, dest_path, basepath)

