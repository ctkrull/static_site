import shutil
import os
import sys
from copystatic import copy_static_recursive, generate_page, generate_pages_recursive
from block_markdown import markdown_text_to_html_node


def main():
    basepath = "/"
    source_path = "./static"
    dest_path = "./docs"

    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    
    print(f"Building site with basepath: {basepath}")
    

    print("Deleting public directory...")
    if os.path.exists(dest_path):
        shutil.rmtree(dest_path)

    print("Copying static files to public directory...")
    copy_static_recursive(source_path, dest_path)

    #Update main.py: after copying files from static to public, it should generate a page from content/index.md using template.html and write it to public/index.html.
    generate_pages_recursive("content", "template.html", "public", basepath)

    #Update your main.sh script to start a simple web server after generating the site. Use the same built-in Python server as before: by adding the following lines to the end of main.sh:
    # print("Starting web server at http://localhost:8000...")
    # python3 src/main.py
    # cd public && python3 -m http.server 8888
    #Change your main function to use generate_pages_recursive instead of generate_page. You should generate a page for every markdown file in the content directory and write the results to the public directory.


main()