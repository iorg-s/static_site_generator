import unittest
from funcions import *
from textnode import *
from htmlnode import *


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_simple_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes[0][0], TextNode("This is text with a ", TextType.TEXT))
        self.assertEqual(new_nodes[0][1], TextNode("code block", TextType.CODE))
        self.assertEqual(new_nodes[0][2], TextNode(" word", TextType.TEXT))

    def test_full_bold(self):
        node = TextNode("**This is a full bold text**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes[0][0] ,TextNode("This is a full bold text", TextType.BOLD))

    def test_bold_start(self):
        node = TextNode("**THIS** is bold", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes[0][0], TextNode("THIS", TextType.BOLD))
        self.assertEqual(new_nodes[0][1], TextNode(" is bold", TextType.TEXT))

    def test_bold_end(self):
        node = TextNode("This is **BOLD**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes[0][0], TextNode("This is ", TextType.TEXT))
        self.assertEqual(new_nodes[0][1], TextNode("BOLD", TextType.BOLD))
    
    def test_no_matching_delimiter(self):
        with self.assertRaises(ValueError) as context:
            new_nodes = split_nodes_delimiter([TextNode("This is **BOLD", TextType.TEXT)], "**", TextType.BOLD)
        self.assertEqual(str(context.exception), "The number of delimeters is odd, perhaps one of them is missing?")