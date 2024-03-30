import re

from enum import Enum

from htmlnode import ParentNode

from textnode import text_to_textnodes, text_node_to_html_node

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks

def block_to_block_type(block):
    if re.match(r"(^#{1,6} \w+)", block):
        return BlockType.HEADING
    if re.match(r"^(```).*(```)$", block):
        return BlockType.CODE
    if block_is_quote(block):
        return BlockType.QUOTE
    if block_is_unordered_list(block):
        return BlockType.UNORDERED_LIST
    if block_is_ordered_list(block):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def block_is_quote(block):
    for line in block.split("\n"):
        if line[0] != ">":
            return False
    return True


def block_is_unordered_list(block):
    for line in block.split("\n"):
        if line[0] != "*" and line[0] != "-":
            return False
    return True

def block_is_ordered_list(block):
    inc = 1
    for line in block.split("\n"):
        if line[0:inc] != "." * inc:
            return False
    return True

def text_to_html_children(text):
    return [text_node_to_html_node(node) for node in text_to_textnodes(text)]

def paragraph_to_html_node(block):
    return ParentNode(tag="p", children=text_to_html_children(block))

def heading_to_html_node(block):
    heading = re.findall(r"^(#{1,6}) (.+)", block)
    return ParentNode(tag=f"h{len(heading[0][0])}", value=text_to_html_children(heading[0][1]))

def code_to_html_node(block):
    code = re.findall(r"^(```)(.*)(```)$", block)
    return ParentNode(tag="pre", children=[ParentNode(tag="code", children=text_to_html_children(code[0][1]))])

def quote_to_html_node(block):
    lines = block.split("\n")
    quote = "\n".join([line.strip(">") for line in lines])
    return ParentNode(tag="blockquote", children=text_to_html_children(quote))

def unordered_list_to_html_node(block):
    return ParentNode(tag="ul", children=[ParentNode(tag="li", children=text_to_html_children(item.strip("*- "))) for item in block.split("\n")])

def ordered_list_to_html_node(block):
    return ParentNode(tag="ol", children=[ParentNode(tag="li", children=text_to_html_children(item.strip(". "))) for item in block.split("\n")])

def block_to_html_node(block):
    converter = {
        BlockType.PARAGRAPH: paragraph_to_html_node,
        BlockType.HEADING: heading_to_html_node,
        BlockType.CODE: code_to_html_node,
        BlockType.QUOTE: quote_to_html_node,
        BlockType.UNORDERED_LIST: unordered_list_to_html_node,
        BlockType.ORDERED_LIST: ordered_list_to_html_node,
    }
    return converter[block_to_block_type(block=block)](block=block)

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    return ParentNode(tag="div", children=[block_to_html_node(block) for block in blocks])