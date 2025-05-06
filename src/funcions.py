import os
import shutil
import re
from htmlnode import *
from textnode import *
from block_type import *

def split_nodes_delimiter(old_nodes, delimiter, text_type):

    new_nodes = []
    for node in old_nodes:
        if node.text.count(delimiter) % 2 != 0:
            raise ValueError("The number of delimeters is odd, perhaps one of them is missing?")
        splited_node_text = node.text.split(delimiter)
        if node.text_type != TextType.TEXT:
            new_nodes.append([node])
        else:
            for text in splited_node_text:
                if text:
                    if f"{delimiter}{text.strip()}{delimiter}" in node.text:
                        new_nodes.append([TextNode(text,text_type)])
                    else:
                        new_nodes.append([TextNode(text,TextType.TEXT)])

    return flatten_list(new_nodes)


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
    link_text = re.findall(r"\[(.*?)\]\((.*?)\)", text)
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
    splitted_text = text.split("\n")
    new_nodes = []
    for text in splitted_text:
        new_nodes.append(TextNode(text, TextType.TEXT))
    # new_nodes = []
    # new_nodes.extend(split_nodes_image([TextNode(text, TextType.TEXT)]))
    for node in new_nodes:
        if extract_markdown_images(node.text):
            new_nodes[new_nodes.index(node)] = split_nodes_image([node])
            new_nodes = flatten_list(new_nodes)
    for node in new_nodes:
        if extract_markdown_links(node.text):
            new_nodes[new_nodes.index(node)] = split_nodes_link([node])
            new_nodes = flatten_list(new_nodes)



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

def quote_to_text(text):
    quote_lines = text.split("\n")
    quote_text = []
    for line in quote_lines:
        if ">" in line:
            quote_text.append(line.strip(">").strip())
        else:
            quote_text.append(line)
    return " ".join(quote_text)

def list_text_to_html(text):
    list_items = text.split("\n")
    list_text = []
    for item in list_items:
        if "- " in item:
            list_text.append("<li>" + item.strip(" -") + "</li>")
        else:
            list_text.append("<li>" + item[3:] + "</li>")
    return "\n".join(list_text)

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:                
            case BlockType.HEADING:
                num = int(re.findall(r"\A#+ ", block)[0].count("#"))
                html_nodes.append(HTMLNode(f"h{num}", block.strip("#").strip()))
            case BlockType.CODE:
                html_nodes.append(HTMLNode("code", block.strip("`").strip()))
            case BlockType.QUOTE:
                html_nodes.append(HTMLNode("blockquote", quote_to_text(block)))
            case BlockType.UNORDERED_LIST:
                html_nodes.append(HTMLNode("ul", block))
            case BlockType.ORDERED_LIST:
                html_nodes.append(HTMLNode("ol", block))
            case _:
                html_nodes.append(HTMLNode("p", " ".join((block.strip()).split("\n")) )) 

    parent_child_nodes = []
    for node in html_nodes:
        if node.tag == "ul" or node.tag == "ol":
            text_value = list_text_to_html(node.value.strip("\\n "))
            nodes = text_to_textnodes(text_value)
            code_node = ""
            for text_node in nodes:
                code_node += (text_node_to_html(text_node).to_html())  
            parent_child_nodes.append(LeafNode(node.tag, code_node))
        elif node.tag == "code":
            code_node = text_node_to_html(TextNode(node.value + "\n", TextType.CODE))
            parent_child_nodes.append(ParentNode("pre", children=[code_node]))
        else:
            child_nodes = text_to_children(node.value)
            parent_child_nodes.append(ParentNode(node.tag, child_nodes))

    return ParentNode("div", children=parent_child_nodes)

def copy_directory(source_directory, destination_directory):
    if os.path.exists(destination_directory):
        shutil.rmtree(destination_directory)

    os.mkdir(destination_directory)
    content = os.listdir(source_directory)
    for item in content:
        if os.path.isfile(os.path.join(source_directory, item)):
            shutil.copy(os.path.join(source_directory, item),destination_directory)
        else:
            copy_directory(os.path.join(source_directory,item), os.path.join(destination_directory, item))
    
def extract_title(markdown):
    header = ""
    lines = markdown.strip().split("\n")
    for line in lines:
        if line.strip().startswith("# "):
            header =  line.strip("#").strip()
    if not header:
        raise SyntaxError("Markdown document does not contain an H1 header.")
    return header

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path} ...")
    file = open(from_path)
    template = open(template_path)
    file_content = file.read()
    template_content = template.read()
    file.close()
    template.close()
    html_string = markdown_to_html_node(file_content).to_html()
    page_title = extract_title(file_content)
    page_content = template_content.replace("{{ Title }}", page_title).replace("{{ Content }}", html_string)
    html_page = open(os.path.join(dest_path, "index.html"), "x")
    html_page.write(page_content)
    html_page.close()

def generate_pages_recursive(dir_path_content = "/home/iorg/workspace/static_site_generator/content", template_path="/home/iorg/workspace/static_site_generator/template.html", dest_dir_path="/home/iorg/workspace/static_site_generator/public"):
    content = os.listdir(dir_path_content)
    for item in content:
        if os.path.isfile(os.path.join(dir_path_content, item)):
            generate_page(os.path.join(dir_path_content, item), template_path, dest_dir_path)
        else:
            if os.path.exists(os.path.join(dest_dir_path, item)):
                shutil.rmtree(os.path.join(dest_dir_path, item))
            os.mkdir(os.path.join(dest_dir_path, item))
            generate_pages_recursive(os.path.join(dir_path_content, item), template_path, os.path.join(dest_dir_path, item))