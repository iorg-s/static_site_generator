import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node1 = HTMLNode("test tag","test value", props={"href":"https://www.google.com", "target": "_blank"})
        node2 = HTMLNode("test tag","test value", props={"href":"https://www.google.com", "target": "_blank"})
        self.assertEqual(node1, node2)

    def test_eq2(self):
        node1 = HTMLNode(tag="")
        node2 = HTMLNode("")
        self.assertEqual(node1, node2)
    
    def test_eq3(self):
        node1 = HTMLNode()
        node2 = HTMLNode()
        self.assertEqual(node1, node2)

    def test_props_to_html(self):
        expected_result = "prop=\"link\" target=\"targ\""
        node = HTMLNode(props={"prop":"link", "target":"targ"})
        self.assertEqual(expected_result, node.props_to_html())
    
    def test_props_to_html2(self):
        expected_result = "img src=\"test.jpg\" alt=\"Test Image\" width=\"200\" height=\"150\""
        node = HTMLNode(props={"img src": "test.jpg", "alt": "Test Image", "width": "200", "height": "150"})
        self.assertEqual(expected_result, node.props_to_html())
    
class TestLeafNode(unittest.TestCase):
  
    def test_leaf_to_html(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html2(self):
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(node.to_html(),"<p>This is a paragraph of text.</p>")

    def test_leaf_to_html3(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "<a href=\"https://www.google.com\">Click me!</a>")

    def test_leaf_to_html4(self): # Tests exception
        with self.assertRaises(ValueError) as context:
            node = LeafNode()
        self.assertEqual(str(context.exception), "Value must be provided")

    def test_eq(self):
        node1 = LeafNode("p", "This is a paragraph of text.")
        node2 = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(node1, node2)


if __name__ == "__main__":
    unittest.main(verbosity=2)