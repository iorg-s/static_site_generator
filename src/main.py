import os
import sys
from textnode import *
from htmlnode import *
from funcions import *

cur_directory = os.getcwd()
copy_path = os.path.join(cur_directory,"static")
target_path = os.path.join(cur_directory,"docs")
template_path = os.path.join(cur_directory, "template.html")
content_path = os.path.join(cur_directory, "content")
default_basepath = "/"

def main():
    basepath = default_basepath
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    copy_directory(copy_path, target_path)

    generate_pages_recursive(content_path, template_path,target_path, basepath)




if __name__ == "__main__":
    main()