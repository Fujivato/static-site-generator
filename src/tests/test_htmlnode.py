import unittest
from src.htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    
    def test_to_html(self):
        node = HTMLNode(tag = "div")
        
        with self.assertRaises(NotImplementedError):
            result = node.to_html()
    
    def test_props_to_html_without_props(self):
        node = HTMLNode(tag = "div")
        expected = ""
        result = node.props_to_html()
        self.assertEqual(expected,result)
        pass
    
    def test_props_to_html_with_props(self):
        props =  { "data-py-id": "test id attribute", "data-py-name": "test name attribute" }      
        node = HTMLNode(tag = "div", props=props)
        expected = 'data-py-id="test id attribute" data-py-name="test name attribute"'
        result = node.props_to_html()
        self.assertEqual(expected,result)
    
    def test_generate_node_tree_with_some_children(self):
        p_node_1_1 = HTMLNode(value = "paragraph 1 text")
        p_node_2_1 = HTMLNode(value = "paragraph 2 text")
        
        p_node_1 = HTMLNode(tag = "p", children=[p_node_1_1])
        p_node_2 = HTMLNode(tag = "p", children=[p_node_2_1])
    
        test_child_nodes = [p_node_1, p_node_2]
        node_tree = HTMLNode(tag = "div", children = test_child_nodes)
        result = node_tree.get_node_tree()
        expected = """HTML Node Tree for div
======================================
<div>
  ↳ <p>
   ↳ <text>
  ↳ <p>
   ↳ <text>"""
        self.assertEqual(expected, result)
    
    def test_generate_node_tree_no_children(self):
        node_tree = HTMLNode(tag = "div")
        result = node_tree.get_node_tree()
        expected = """HTML Node Tree for div
======================================
<div>"""
        self.assertEqual(expected,result)
    
    def test_repr_without_props(self):
        test_node = HTMLNode(tag = "span", value="hello world")
        result = f"{test_node}"
        expected = "HTMLNode(span, hello world)"
        self.assertEqual(result, expected)
    
    def test_repr_with_props(self):
        test_props = { "data-py-id": "test id attribute", "data-py-name": "test name attribute" }
        
        # tag, value, children, props
        test_node = HTMLNode(tag = "div", props = test_props)
        result = f"{test_node}"
        expected = """HTMLNode(div, None)
  Props:
     "data-py-id": "test id attribute"
     "data-py-name": "test name attribute"
"""
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()