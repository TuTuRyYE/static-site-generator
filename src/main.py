import os

from markdown import markdown_to_html_node, extract_title
from copy_static import copy_directory


def main():
    copy_directory("./static", "./public")
    generate_pages_recursive("./content", "template.html", "./public")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    file = open(from_path, 'r')
    content = file.read()
    file.close()

    file = open(template_path, 'r')
    template = file.read()
    file.close()
    
    html_content = markdown_to_html_node(content).to_html()

    template = template.replace("{{ Title }}", extract_title(content))
    template = template.replace("{{ Content }}", html_content)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    file = open(dest_path, 'w')
    file.write(template)
    file.close()

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if not os.path.exists(dir_path_content) and not os.path.exists(dest_dir_path) and not os.path.exists(template_path):
        raise ValueError("one of the specified paths does not exist")
    
    for d in os.listdir(dir_path_content):
        current_path = os.path.join(dir_path_content, d)
        if os.path.isfile(current_path):
            generate_page(current_path, template_path, os.path.join(dest_dir_path, "index.html"))
        else:
            generate_pages_recursive(current_path, template_path, os.path.join(dest_dir_path, d))


if __name__ == "__main__":
    main()