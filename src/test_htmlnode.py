import unittest

from htmlnode import HTMLNode


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
    
        



if __name__ == "__main__":
    unittest.main(verbosity=2)