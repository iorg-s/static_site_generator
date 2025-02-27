from textnode import *
from htmlnode import *

def main():
    try:
        my_text_node = TextNode("This is a text node", "bold", "https://www.boot.dev")
        print(my_text_node)
    except AttributeError:
        print("TEXT_TYPE must be one of this: NORMAL, BOLD, ITALIC, CODE, LINK, IMAGE")


    

if __name__ == "__main__":
    main()