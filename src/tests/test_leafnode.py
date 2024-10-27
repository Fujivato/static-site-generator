import unittest
from src.leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def to_html_without_value(self):
        node = LeafNode(tag = "p")
        
        with self.assertRaises(ValueError):
            result = node.to_html()
    
    def to_html_with_value(self):
        node = LeafNode(tag = "p", value = "Hello World")
        result = node.to_html()
        expected = "<p>Hello World</p>"
        self.assertEqual(expected, result)
    
    def to_html_without_tag(self):
        node = LeafNode(value = "Hello World")
        result = node.to_html()
        expected = "Hello World"
        self.assertEqual(expected, result)
      
    def to_html_with_tag_and_props(self):
        node = LeafNode(tag = "a", value = "Click me!", props = {"href": "https://www.google.com"})
        result = node.to_html()
        expected = '<a href="https://www.google.com">Click me!</a>'
        self.assertEqual(expected, result)
    
if __name__ == "__main__":
    unittest.main()
