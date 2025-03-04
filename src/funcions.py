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