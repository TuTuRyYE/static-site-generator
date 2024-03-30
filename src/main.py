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


if __name__ == "__main__":
    main()