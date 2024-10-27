import unittest
from src.parentnode import ParentNode
from src.leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_to_html_adds_props_to_nodes(self):
        child_node = LeafNode(tag = "p", value="Hello World")
        div_node = ParentNode(tag = "div", children=[child_node], props={ "id": "py-parent", "name": "py-name" })
        result = div_node.to_html()
        expected = """<div id="py-parent" name="py-name"><p>Hello World</p></div>"""
        self.assertEqual(expected, result)

    def test_to_html_adds_props_to_child_nodes(self):
        child_text = LeafNode(value = "Boot.dev is great!")
        child_paragraph = ParentNode(tag = "p", children=[child_text], props = { "style": "border-radius: 4px; font-weight:700;" })
        div_node = ParentNode(tag = "div", children=[child_paragraph])
        result = div_node.to_html()
        expected = """<div><p style="border-radius: 4px; font-weight:700;">Boot.dev is great!</p></div>"""
        self.assertEqual(expected, result)
    
    def test_to_html_renders_all_parent_node_trees(self):
        child_two_node_one = LeafNode(tag = "code", value="print('hello world!')")
        div_two = ParentNode(tag = "div", children=[child_two_node_one])
        child_one_node_one_c2 = LeafNode(tag = "li", value="List Item Two")
        child_one_node_one_c1 = LeafNode(tag = "li", value="List Item One")
        child_one_node_one = ParentNode(tag = "ul", children=[child_one_node_one_c1, child_one_node_one_c2])
        div_one = ParentNode(tag = "div", children=[child_one_node_one, div_two])
        expected = """<div><ul><li>List Item One</li><li>List Item Two</li></ul><div><code>print('hello world!')</code></div></div>"""
        result = div_one.to_html()
        self.assertEqual(expected, result)
    
    def test_to_html_renders_multiple_children(self):
        child_two_node_one = LeafNode(tag = "code", value="print('hello world!')")
        child_one_node_one_c2 = LeafNode(tag = "li", value="List Item Two")
        child_one_node_one_c1 = LeafNode(tag = "li", value="List Item One")
        child_one_node_one = ParentNode(tag = "ul", children=[child_one_node_one_c1, child_one_node_one_c2])
        div_one = ParentNode(tag = "div", children=[child_one_node_one, child_two_node_one])
        expected = """<div><ul><li>List Item One</li><li>List Item Two</li></ul><code>print('hello world!')</code></div>"""
        result = div_one.to_html()
        self.assertEqual(expected, result)
    
    def test_to_html_renders_no_children(self):
        node = ParentNode(tag = "div", children=[], props={ "id": "py-div-one", "name": "py-div-name" })
        
        with self.assertRaises(ValueError):
            result = node.to_html()
        
    def test_to_html_renders_plain_text(self):
        text_node_three = LeafNode(value="the lazy dog")
        text_node_two = LeafNode(value="fox jumps over")
        text_node_one = LeafNode(value="The quick brown")
        node = ParentNode(tag = "div", children=[text_node_one, text_node_two, text_node_three])
        expected="""<div>The quick brown fox jumps over the lazy dog</div>"""
        result = node.to_html()
        self.assertEqual(expected, result)
    
    def test_to_html_adds_value_to_printed_node(self):
        child_node = LeafNode(value="Hello Universe.")
        div_node = ParentNode(tag = "div",children=[child_node])
        expected = """<div>Hello Universe.</div>"""
        result = div_node.to_html()
        self.assertEqual(expected, result)
    
    def test_to_html_adds_value_to_child_nodes(self):
        child_node = LeafNode(tag = "p", value="Hello World!")
        div_node = ParentNode(tag = "div", children=[child_node])
        result = div_node.to_html()
        expected = """<div><p>Hello World!</p></div>"""
        self.assertEqual(expected, result)
    
    def test_boot_dev_check(self):
        node = ParentNode(
        "p", 
        [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ])
        expected = """<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"""
        result = node.to_html()
        self.assertEqual(expected, result)
    
if __name__ == "__main__":
    unittest.main()
