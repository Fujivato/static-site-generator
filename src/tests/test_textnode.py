import unittest
from src.textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a test node", TextType.ITALIC, "http://www.example.com")
        node2 = TextNode("This is a test node", TextType.ITALIC, "HTTP://www.Example.cOm")
        self.assertEqual(node, node2)
        
    def test_not_eq(self):
        node = TextNode("This is a test node", TextType.BOLD)
        node2 = TextNode("This is a new test node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_url(self):
        node = TextNode("This is a test node", TextType.BOLD, "https://example.com")
        node2 = TextNode("This is a test node", TextType.BOLD, "https://www.sample.com")
        self.assertNotEqual(node, node2)

    def test_not_eq_type(self):
        node = TextNode("This is a test node", TextType.BOLD, "https://example.com")
        node2 = TextNode("This is a test node", TextType.ITALIC, "https://www.sample.com")
        self.assertNotEqual(node, node2)
        
    def test_to_string(self):
        node = TextNode("This is a test node", TextType.BOLD)
        result = str(node)
        self.assertEqual(result, 'TextNode("This is a test node", TextType.BOLD, None)')
    
    def test_to_string_url(self):
        node = TextNode("This is a test node", TextType.BOLD, "https://www.sample.com")
        result = str(node)
        self.assertEqual(result, 'TextNode("This is a test node", TextType.BOLD, "https://www.sample.com")')
    
if __name__ == "__main__":
    unittest.main()
