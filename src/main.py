from textnode import TextNode, TextNodeType, text_to_textnodes

def main():
    text = "This is **text** with an *italic* word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
    print('[')
    for node in text_to_textnodes(text):
        print(f"   {node}")
    print(']')

if __name__ == "__main__":
    main()