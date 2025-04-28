import re
from htmlnode import *
from textnode import *
from block_type import *

def split_nodes_delimiter(old_nodes, delimiter, text_type):

    new_nodes = []
    for node in old_nodes:
        if node.text.count(delimiter) % 2 != 0:
            print(f"{delimiter} count is {node.text.count(delimiter)}")
            raise ValueError("The number of delimeters is odd, perhaps one of them is missing?")
        splited_node_text = node.text.split(delimiter)
        if node.text_type != TextType.TEXT:
            new_nodes.append([node])
        else:
            if splited_node_text[0] == "" and splited_node_text[2] == "":
                new_nodes.append([TextNode(splited_node_text[1], text_type)])
            elif splited_node_text[0] == "" and splited_node_text[2] != "":
                new_nodes.append(
                    [
                        TextNode(splited_node_text[1], text_type),
                        TextNode(splited_node_text[2], TextType.TEXT)
                    ]
                )
            elif splited_node_text[0] != "" and splited_node_text[2] == "":
                new_nodes.append(
                    [
                        TextNode(splited_node_text[0], TextType.TEXT),
                        TextNode(splited_node_text[1], text_type)
                    ]
                )
            else :
                new_nodes.append(
                    [
                        TextNode(splited_node_text[0], TextType.TEXT),
                        TextNode(splited_node_text[1], text_type),
                        TextNode(splited_node_text[2], TextType.TEXT)
                    ]
                )
    return new_nodes


def extract_markdown_images(text):
    image_text = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    text_list = []
    link_list = []
    for image in image_text:
        text_list.append(image[0])
        link_list.append(image[1]) 
    text_link_list = list(zip(text_list, link_list))                  
    return text_link_list

def extract_markdown_links(text):
    link_text = re.findall(r"\s\[(.*?)\]\((.*?)\)", text)
    text_list = []
    link_list = []
    for link in link_text:
        text_list.append(link[0])
        link_list.append(link[1])
    text_link_list = list(zip(text_list, link_list))
    return text_link_list

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        image = extract_markdown_images(node.text)
        if image == []:
            new_nodes.append(node)
            continue
        alt_text, url = image[0] 
        full_image_block = f"![{alt_text}]({url})"
        text_before = node.text[:node.text.find(full_image_block)]
        text_after = node.text[len(text_before) +  len(full_image_block):] 
        if extract_markdown_images(text_after):
            if not text_after and not text_before:
                new_nodes.extend([
                    TextNode(alt_text, TextType.IMAGE, url)
                ])
            elif not text_before:
                new_nodes.extend([
                    TextNode(alt_text, TextType.IMAGE, url),
                    TextNode(text_after, TextType.TEXT)
                ]) 
            elif not text_after:
                new_nodes.extend([
                    TextNode(text_before, TextType.TEXT),
                    TextNode(alt_text, TextType.IMAGE, url),
                ])
            else:
                new_nodes.extend([
                        TextNode(text_before, TextType.TEXT),
                        TextNode(alt_text, TextType.IMAGE, url),
                    ])
                new_nodes.extend(split_nodes_image([TextNode(text_after,TextType.TEXT)]))
        else:
                if not text_after and not text_before:
                    new_nodes.extend([
                        TextNode(alt_text, TextType.IMAGE, url)
                    ])
                elif not text_before:
                    new_nodes.extend([
                    TextNode(alt_text, TextType.IMAGE, url),
                    TextNode(text_after, TextType.TEXT)
                ]) 
                elif not text_after:
                    new_nodes.extend([
                        TextNode(text_before, TextType.TEXT),
                        TextNode(alt_text, TextType.IMAGE, url),
                    ])
                else: 
                    new_nodes.extend([
                        TextNode(text_before, TextType.TEXT),
                        TextNode(alt_text, TextType.IMAGE, url),
                        TextNode(text_after, TextType.TEXT)
                    ])
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        link = extract_markdown_links(node.text)
        if not link:
            new_nodes.append(node)
        link_text, url = link[0] 
        full_link_block = f"[{link_text}]({url})"
        text_before = node.text[:node.text.find(full_link_block)]
        text_after = node.text[len(text_before) +  len(full_link_block):] 
        if extract_markdown_links(text_after):
            if not text_after and not text_before:
                new_nodes.extend([
                    TextNode(link_text, TextType.LINK, url)
                ])
            elif not text_before:
                new_nodes.extend([
                    TextNode(link_text, TextType.LINK, url),
                    TextNode(text_after, TextType.TEXT)
                ]) 
            elif not text_after:
                new_nodes.extend([
                    TextNode(text_before, TextType.TEXT),
                    TextNode(link_text, TextType.LINK, url),
                ])
            else:
                new_nodes.extend([
                        TextNode(text_before, TextType.TEXT),
                        TextNode(link_text, TextType.LINK, url),
                    ])
                new_nodes.extend(split_nodes_link([TextNode(text_after,TextType.TEXT)]))
        else:
                if not text_after and not text_before:
                    new_nodes.extend([
                        TextNode(link_text, TextType.LINK, url)
                    ])
                elif not text_before:
                    new_nodes.extend([
                    TextNode(link_text, TextType.LINK, url),
                    TextNode(text_after, TextType.TEXT)
                ]) 
                elif not text_after:
                    new_nodes.extend([
                        TextNode(text_before, TextType.TEXT),
                        TextNode(link_text, TextType.LINK, url),
                    ])
                else: 
                    new_nodes.extend([
                        TextNode(text_before, TextType.TEXT),
                        TextNode(link_text, TextType.LINK, url),
                        TextNode(text_after, TextType.TEXT)
                    ])
    return new_nodes

def flatten_list(nodes):
        new_nodes = []
        for node in nodes:
            if type(node) == TextNode:
                new_nodes.append(node)
            else:
                new_nodes.extend(flatten_list(node))
        return new_nodes

def text_to_textnodes(text):
    new_nodes = []
    new_nodes.extend(split_nodes_image([TextNode(text, TextType.TEXT)]))
    for node in new_nodes:
        if extract_markdown_links(node.text):
            new_nodes[new_nodes.index(node)] = split_nodes_link([node])


    new_nodes = flatten_list(new_nodes)
    num_of_delimiters = 3
    for i in range(num_of_delimiters):
        for node in new_nodes:
            if "**" in node.text:
                new_nodes[new_nodes.index(node)] = split_nodes_delimiter([node], "**", TextType.BOLD)
                new_nodes = flatten_list(new_nodes)
            elif "_" in node.text:
                new_nodes[new_nodes.index(node)] = split_nodes_delimiter([node], "_", TextType.ITALIC)
                new_nodes = flatten_list(new_nodes)
            elif "`" in node.text:
                new_nodes[new_nodes.index(node)] = split_nodes_delimiter([node], "`", TextType.CODE)
                new_nodes = flatten_list(new_nodes)
               
    return new_nodes

def markdown_to_blocks(markdown):
    blocks = []
    lines = markdown.strip().split("\n\n")
    full_list = []
    full_paragraph = []
    for line in lines:
        # splits every splitted block from markdown on new line i.e. checks if a block spans on multiple lines
        block_lines = line.split("\n")
        # if len == 1 then one line = one block
        if len(block_lines) == 1:
            blocks.append(line.strip())   
        else:
            for line in block_lines:
                line = line.strip()

                if line.startswith("-"):
                    full_list.append(line)
                else: 
                    full_paragraph.append(line)

            if len(full_list) != 0: 
                blocks.append("\n".join(full_list))
            if len(full_paragraph) != 0:
                blocks.append("\n".join(full_paragraph))
            
            full_paragraph = []
            full_list = []

    return blocks

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for node in text_nodes:
        html_nodes.append(text_node_to_html(node))
     
    return html_nodes 

def list_text_to_html(text):
    list_items = text.split("\n")
    list_text = []
    for item in list_items:
        if "- " in item:
            list_text.append("<li>" + item.strip(" -") + "</li>")
        else:
            list_text.append("<li>" + item[3:] + "</li>")
    return "".join(list_text)

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:                
            case BlockType.HEADING:
                num = int(re.findall("\A#+ ", block)[0].count("#"))
                html_nodes.append(HTMLNode(f"h{num}", block.strip("#").strip()))
            case BlockType.CODE:
                html_nodes.append(HTMLNode("code", block.strip("`").strip()))
            case BlockType.QUOTE:
                html_nodes.append(HTMLNode("blockquote", block))
            case BlockType.UNORDERED_LIST:
                html_nodes.append(HTMLNode("ul", list_text_to_html(block)))
            case BlockType.ORDERED_LIST:
                html_nodes.append(HTMLNode("ol", list_text_to_html(block)))
            case _:
                html_nodes.append(HTMLNode("p", " ".join((block.strip()).split("\n")) )) 

    parent_child_nodes = []
    for node in html_nodes:
        if node.tag == "code":
            code_node = text_node_to_html(TextNode(node.value + "\n", TextType.CODE))
            parent_child_nodes.append(ParentNode("pre", children=[code_node]))
        else:
            child_nodes = text_to_children(node.value)
            parent_child_nodes.append(ParentNode(node.tag, child_nodes))

    return ParentNode("div", children=parent_child_nodes)