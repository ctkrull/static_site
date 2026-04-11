# 'unittest' is a built-in Python library used to verify that our code works as expected.
import unittest

# We import our own classes so we can create objects to test.
from textnode import TextNode, TextType, text_node_to_html_node



class TestTextNode(unittest.TestCase):
    # This test checks the "Happy Path": 
    # If two nodes have the exact same data, they SHOULD be equal.
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        # assertEqual fails if node == node2 is False.
        self.assertEqual(node, node2)

    # Edge Case: Same type, but the text is different.
    def test_not_eq_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        # assertNotEqual passes if the nodes are different.
        self.assertNotEqual(node, node2)

    # Edge Case: Same text, but one is BOLD and one is ITALIC.
    def test_not_eq_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    # Edge Case: Everything matches except the URL.
    # This proves our __eq__ method is actually looking at the URL field.
    def test_not_eq_url(self):
        node = TextNode("This is a text node", TextType.LINK, "https://www.google.com")
        node2 = TextNode("This is a text node", TextType.LINK, "https://www.boot.dev")
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold text") 

    def test_italic(self):
        node = TextNode("This is italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is italic text")

    def test_code(self):
        node = TextNode("print('Hello, world!')", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('Hello, world!')")

    def test_link(self):
        node = TextNode("Google", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Google")
        self.assertEqual(html_node.props, {"href": "https://www.google.com"})

    def test_image(self):
        node = TextNode("Alt text", TextType.IMAGE, "https://www.google.com/image.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.props, {"src": "https://www.google.com/image.jpg", "alt": "Alt text"})

  

    


# This line tells Python: "If I run this file directly (not just importing it), 
# then go ahead and execute all the tests defined above."
if __name__ == "__main__":
    unittest.main()