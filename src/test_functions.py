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
    

    class TestExtractFuction(unittest.TestCase):
        def test_extract(self):
            matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
            self.assertEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
        
        def test_extract_no_text(self):
            matches = extract_markdown_images("This is text with an ![](https://i.imgur.com/zjjcJKZ.png)")
            self.assertListEqual([("", "https://i.imgur.com/zjjcJKZ.png")], matches)
        
        def test_extract_with_a_lot_of_staff(self):
            matches = extract_markdown_images("This is text with an ![1234 !@#$%^&*) hello wordl](https://i.imgur.com/zjjcJKZ.png)")
            self.assertListEqual([("1234 !@#$%^&*) hello wordl", "https://i.imgur.com/zjjcJKZ.png")], matches)
        
        def extract_link(self):
            matches = extract_markdown_links("This is text with an [link](https://i.imgur.com/zjjcJKZ.png)")
            self.assertListEqual([("", "https://i.imgur.com/zjjcJKZ.png")], matches)

        def extract_links(self):
            matches = extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
            self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube","https://www.youtube.com/@bootdotdev")], matches)
        
        def extract_link_from_image(self):
            matches = extract_markdown_images("This is text with an ![link](https://i.imgur.com/zjjcJKZ.png)")
            self.assertListEqual([("", "https://i.imgur.com/zjjcJKZ.png")], matches)


class TestSplitText(unittest.TestCase):
    def test_split_one_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")
            ],
            new_nodes
        )
    def test_split_several_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_several_images_no_text(self):
        node = TextNode(
            "This is text with two images ![image](https://i.imgur.com/zjjcJKZ.png), ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
                [
                    TextNode("This is text with two images ", TextType.TEXT),
                    TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                    TextNode(", ", TextType.TEXT),
                    TextNode(
                        "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                    ),
                ],
                new_nodes,
            )
    def test_split_one_image_and_text_after(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and some text.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and some text.", TextType.TEXT)
            ],
            new_nodes
        )
    def test_split_one_image_and_text_before(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) and then some text.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and then some text.", TextType.TEXT)
            ],
            new_nodes
        )
    def test_split_just_one_image(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes
        )

    def test_split_links(self):
        node = TextNode(
        "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
        TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
         [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
         ], 
         new_nodes
    )
        
    def test_text_to_text_node(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        text_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            text_nodes
        )