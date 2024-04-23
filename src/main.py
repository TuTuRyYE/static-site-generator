import os
import shutil

from textnode import TextNode, TextNodeType, text_to_textnodes
from markdown import markdown_to_html_node


def main():
    text = "This is **text** with an *italic* word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
    print('[')
    for node in text_to_textnodes(text):
        print(f"   {node}")
    print(']')
    text_markdown = '''
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
'''
    print(markdown_to_html_node(text_markdown).to_html())
    copy_directory("./static", "./public")


def copy_directory(src, dest):
    if not os.path.exists(src):
        raise ValueError("src does not exist")
    if os.path.isfile(dest) or os.path.isfile(src):
        raise ValueError("src and dest must be a directory")
    if os.path.exists(dest):
        shutil.rmtree(dest, ignore_errors=True)
    
    os.mkdir(dest)
    
    for d in os.listdir(src):
        if os.path.isfile(os.path.join(src, d)):
            shutil.copy(os.path.join(src, d), dest)
        else:
            copy_directory(os.path.join(src, d), os.path.join(dest, d))


if __name__ == "__main__":
    main()