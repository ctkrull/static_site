# 'unittest' is a built-in Python library used to verify that our code works as expected.
import unittest

# We import our own classes so we can create objects to test.
from textnode import TextNode, TextType, text_node_to_html_node
from text_textnode import text_to_textnodes
from split_delimiter import split_nodes_delimiter
from extract_markdown import extract_markdown_images, extract_markdown_links
from split_nodes import split_nodes_image, split_nodes_link




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

    def test_split_delimiter(self):
        node = TextNode("This is `code` and more `code`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        # You should get 4 nodes back: Text, Code, Text, Code
        self.assertEqual(len(new_nodes), 4)
        self.assertEqual(new_nodes[1].text, "code")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)

    def test_text_to_textnodes_parser(self):
        text = (
            "This is **text** with an *italic* word and a `code block` "
            "and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) "
            "and a [link](https://boot.dev)"
        )
        nodes = text_to_textnodes(text)

        expected = [
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
        ]

        self.assertEqual(nodes, expected)

    # def test_extract_markdown_images(self):
    #     text = "Here is an image: ![Alt text](https://www.example.com/image.jpg)"
    #     images = extract_markdown_images(text)
    #     self.assertEqual(len(images), 1)
    #     self.assertEqual(images[0]['alt'], "Alt text")
    #     self.assertEqual(images[0]['url'], "https://www.example.com/image.jpg")

    def test_extract_markdown_links(self):
        text = "Here is a link: [Google](https://www.google.com)"
        links = extract_markdown_links(text)
        self.assertEqual(len(links), 1)
        self.assertEqual(links[0]['text'], "Google")
        self.assertEqual(links[0]['url'], "https://www.google.com")

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)", TextType.TEXT,)
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
    
    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://www.google.com) and another [second link](https://www.boot.dev)",
            TextType.TEXT,)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.google.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://www.boot.dev"
                ),
            ],
            new_nodes,
        )

    def test_split_links_and_images(self):
        node = TextNode(
            "This is text with a [link](https://www.google.com) and an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,)
        new_nodes = split_nodes_link(split_nodes_image([node]))
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.google.com"),
                TextNode(" and an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )
  
    def test_split_links_and_images_reversed(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://www.google.com)",
            TextType.TEXT,)
        new_nodes = split_nodes_image(split_nodes_link([node]))
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.google.com"),
            ],
            new_nodes,
        )

    # def test_split_links_and_images_with_code(self):
    #     node = TextNode(
    #         "This is text with a [link](https://www.google.com), an ![image](https://i.imgur.com/zjjcJKZ.png), and some `code`",
    #         TextType.TEXT,)
    #     new_nodes = split_nodes_image(split_nodes_link(split_nodes_delimiter([node], "`", TextType.CODE)))
    #     self.assertListEqual(
    #         [
    #             TextNode("This is text with a ", TextType.TEXT),
    #             TextNode("link", TextType.LINK, "https://www.google.com"),
    #             TextNode(", an ", TextType.TEXT),
    #             TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
    #             TextNode(", and some ", TextType.TEXT),
    #             TextNode("code", TextType.CODE),
    #         ],
    #         new_nodes,
    #     )

    # def test_split_links_and_images_with_code_reversed(self):
    #     node = TextNode(
    #         "This is text with some `code`, an ![image](https://i.imgur.com/zjjcJKZ.png), and a [link](https://www.google.com)",
    #         TextType.TEXT,)
    #     new_nodes = split_nodes_link(split_nodes_image(split_nodes_delimiter([node], "`", TextType.CODE)))
    #     self.assertListEqual(
    #         [
    #             TextNode("This is text with some ", TextType.TEXT),
    #             TextNode("code", TextType.CODE),
    #             TextNode(", an ", TextType.TEXT),
    #             TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
    #             TextNode(", and a ", TextType.TEXT),
    #             TextNode("link", TextType.LINK, "https://www.google.com"),
    #         ],
    #         new_nodes,
    #     )
    


# This line tells Python: "If I run this file directly (not just importing it), 
# then go ahead and execute all the tests defined above."
if __name__ == "__main__":
    unittest.main()