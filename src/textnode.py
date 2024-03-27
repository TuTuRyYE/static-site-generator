import re

from enum import Enum

from htmlnode import LeafNode


class TextNodeType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode():
    def __init__(self, text, text_type, url=None) -> None:
        self.text = text
        self.text_type = TextNodeType(text_type)
        self.url = url
    
    def __eq__(self, text_node) -> bool:
        return self.text == text_node.text and self.text_type == text_node.text_type and self.url == text_node.url

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
    

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextNodeType.TEXT:
            return LeafNode(tag=None, value=text_node.text)
        case TextNodeType.BOLD:
            return LeafNode(tag="b", value=text_node.text)
        case TextNodeType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        case TextNodeType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        case TextNodeType.LINK:
            return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
        case TextNodeType.IMAGE:
            return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})
    raise Exception("text node type not invalid")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextNodeType.TEXT:
            nodes.append(old_node)
            continue
        text = old_node.text
        while True:
            splitted = text.split(delimiter, 2)
            if len(splitted) != 3 and len(splitted) != 1:
                raise Exception("no closing delimiter found")
            if len(splitted) == 1:
                if len(text) > 0:
                    nodes.append(TextNode(text, TextNodeType.TEXT))
                break
            
            nodes.append(TextNode(splitted[0], TextNodeType.TEXT))
            nodes.append(TextNode(splitted[1], text_type))
            text = splitted[2]

    return nodes

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)

def split_nodes_image(old_nodes):
    nodes = []
    for old_node in old_nodes:
        text = old_node.text
        images = extract_markdown_images(text)
        if len(images) == 0:
            nodes.append(old_node)
            continue
        for image in images:
            splitted = text.split(f"![{image[0]}]({image[1]})", 1)
            if len(splitted[0]) > 0:
                nodes.append(TextNode(splitted[0], TextNodeType.TEXT))
            nodes.append(TextNode(image[0], TextNodeType.IMAGE, image[1]))
            text = splitted[1]
        if len(text) > 0:
            nodes.append(TextNode(text, TextNodeType.TEXT))


    return nodes

def split_nodes_link(old_nodes):
    nodes = []
    for old_node in old_nodes:
        text = old_node.text
        links = extract_markdown_links(text)
        if len(links) == 0:
            nodes.append(old_node)
            continue
        for link in links:
            splitted = text.split(f"[{link[0]}]({link[1]})", 1)
            if len(splitted[0]) > 0:
                nodes.append(TextNode(splitted[0], TextNodeType.TEXT))
            nodes.append(TextNode(link[0], TextNodeType.LINK, link[1]))
            text = splitted[1]
        if len(text) > 0:
            nodes.append(TextNode(text, TextNodeType.TEXT))

    return nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextNodeType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextNodeType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextNodeType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextNodeType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes