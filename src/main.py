import shutil
import os
from copystatic import copy_static_recursive, generate_page
from block_markdown import markdown_text_to_html_node


def main():
    source_path = "./static"
    dest_path = "./public"

    print("Deleting public directory...")
    if os.path.exists(dest_path):
        shutil.rmtree(dest_path)

    print("Copying static files to public directory...")
    copy_static_recursive(source_path, dest_path)

    #Update main.py: after copying files from static to public, it should generate a page from content/index.md using template.html and write it to public/index.html.
    from copystatic import generate_page
    generate_page("content/index.md", "template.html", "public/index.html")

    #Update your main.sh script to start a simple web server after generating the site. Use the same built-in Python server as before: by adding the following lines to the end of main.sh:
    # print("Starting web server at http://localhost:8000...")
    # python3 src/main.py
    # cd public && python3 -m http.server 8888


main()