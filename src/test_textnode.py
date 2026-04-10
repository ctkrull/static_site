# 'unittest' is a built-in Python library used to verify that our code works as expected.
import unittest

# We import our own classes so we can create objects to test.
from textnode import TextNode, TextType


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

# This line tells Python: "If I run this file directly (not just importing it), 
# then go ahead and execute all the tests defined above."
if __name__ == "__main__":
    unittest.main()