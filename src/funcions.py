import re
from htmlnode import *
from textnode import *

def split_nodes_delimiter(old_nodes, delimiter, text_type):

    new_nodes = []
    for node in old_nodes:
        if node.text.count(delimiter) != 2:
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
        if not image:
            new_nodes.append(node)
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
