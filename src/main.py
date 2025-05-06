import os
from textnode import *
from htmlnode import *
from funcions import *

def main():

    cur_directory = os.getcwd()
    copy_path = os.path.join(cur_directory, "static")
    target_path = os.path.join(cur_directory, "public")
    copy_directory(copy_path, target_path)
    template_path = os.path.join(cur_directory, "template.html")
    content_path = os.path.join(cur_directory, "content")
    generate_pages_recursive(content_path, template_path,target_path)




if __name__ == "__main__":
    main()