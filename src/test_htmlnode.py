import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        # 1. We define what the 'Input' looks like (a Python Dictionary)
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        # 2. We create the node with those props
        node = HTMLNode(props=props)
        
        # 3. We define what the 'Expected Output' string must look like
        # (Based on the pattern: space key equals quote value quote)
        expected = ' href="https://www.google.com" target="_blank"'
        
        # 4. We check if our method actually produces that string
        self.assertEqual(node.props_to_html(), expected)

    def test_values(self):
        # Test that the values we put in are the values we get out
        node = HTMLNode("div", "I am a div")
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "I am a div")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_repr(self):
        # Test that our __repr__ (the print string) looks how we expect
        node = HTMLNode("p", "What a nice paragraph", None, {"class": "primary"})
        # This just makes sure the string output contains the info we need for debugging
        self.assertEqual(
            repr(node),
            "HTMLNode(p, What a nice paragraph, children: None, {'class': 'primary'})"
        )

    def test_leaf_to_html_p(self):
        # We want to see if <p>This is a paragraph</p> comes out.
        node = LeafNode("p", "This is a paragraph")
        self.assertEqual(node.to_html(), "<p>This is a paragraph</p>")

    def test_leaf_to_html_link(self):
        # This checks if the props (the dictionary) get added correctly.
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_parent_to_html(self):
        # This checks if the parent node renders correctly with its children
        child1 = LeafNode("p", "First paragraph")
        child2 = LeafNode("p", "Second paragraph")
        node = ParentNode("div", [child1, child2])
        self.assertEqual(node.to_html(), "<div><p>First paragraph</p><p>Second paragraph</p></div>")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(),"<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_props(self):
        child_node = LeafNode("a", "Google", {"href": "https://www.google.com"})
        parent_node = ParentNode("div", [child_node], {"class": "container"})
        self.assertEqual(parent_node.to_html(), '<div class="container"><a href="https://www.google.com">Google</a></div>',
        )

    def test_to_html_with_empty_children(self):
        parent_node = ParentNode("div", [])
        self.assertEqual(parent_node.to_html(), "<div></div>")  

    def test_to_html_with_none_children(self):
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()  

    def test_to_html_with_none_tag(self):
        with self.assertRaises(ValueError):
            ParentNode(None, []).to_html()

    def test_leaf_to_html_with_none_value(self):
        with self.assertRaises(ValueError):
            LeafNode("p", None).to_html()





if __name__ == "__main__":
    unittest.main()