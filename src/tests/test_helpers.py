import unittest
from src.helpers import text_node_to_html_node
from src.helpers import split_nodes_delimeter
from src.helpers import extract_markdown_images
from src.helpers import extract_markdown_links
from src.helpers import split_nodes_image
from src.helpers import split_nodes_link
from src.helpers import text_to_textnodes
from src.helpers import markdown_to_blocks
from src.helpers import block_to_block_type
from src.helpers import text_to_children
from src.helpers import markdown_to_html_node
from src.textnode import TextType, TextNode
from src.leafnode import LeafNode
from src.blocktype import BlockType

class TestHelpers(unittest.TestCase):
    # Tests for text_node_to_html_node
    def test_text_type_text_renders_no_tag(self):      
        text_node = TextNode(text = "Hello World", text_type = TextType.TEXT)
        result = text_node_to_html_node(text_node)
        self.assertIsInstance(result, LeafNode)
        self.assertEqual(None, result.tag)

    def test_text_type_bold_renders_bold(self):
        text_node = TextNode(text = "Hello World", text_type = TextType.BOLD)
        result = text_node_to_html_node(text_node)
        self.assertIsInstance(result, LeafNode)
        self.assertEqual("b", result.tag)
    
    def test_text_type_italic_renders_italic(self):
        text_node = TextNode(text = "Hello World", text_type = TextType.ITALIC)
        result = text_node_to_html_node(text_node)
        self.assertIsInstance(result, LeafNode)
        self.assertEqual("i", result.tag)
    
    def test_text_type_code_renders_code(self):
        text_node = TextNode(text = "Hello World", text_type = TextType.CODE)
        result = text_node_to_html_node(text_node)
        self.assertIsInstance(result, LeafNode)
        self.assertEqual("code", result.tag)
    
    def test_text_type_link_renders_link(self):
        text_node = TextNode(text = "Hello World", text_type = TextType.LINK, url = "http://www.sample.com")
        result = text_node_to_html_node(text_node)
        self.assertIsInstance(result, LeafNode)
        self.assertEqual("a", result.tag)
    
    def test_text_type_link_uses_url(self):
        text_node = TextNode(text = "Hello World", text_type = TextType.LINK, url = "http://www.sample.com")
        result = text_node_to_html_node(text_node)
        expected_props = { "href": "http://www.sample.com" }
        self.assertIsInstance(result, LeafNode)
        self.assertDictEqual(expected_props, result.props)
     
    def test_text_type_img_renders_img(self):
        text_node = TextNode(text = "Hello World", text_type = TextType.IMAGE)
        result = text_node_to_html_node(text_node)
        self.assertIsInstance(result, LeafNode)
        self.assertEqual("img", result.tag)
        
    def test_text_type_image_uses_value_and_url(self):
        text_node = TextNode(text = "Hello World", text_type = TextType.IMAGE, url="http://www.sample.com")
        result = text_node_to_html_node(text_node)
        self.assertIsInstance(result, LeafNode)
        expected_props = { "src": "http://www.sample.com", "alt": "Hello World" }
        self.assertDictEqual(expected_props, result.props)
    
    # Tests for split_nodes_delimeter
    
    # [x] splits a node based on a delimiter
    # [x] create a new node based on text_type
    # [x] create a new node with value of delimited type
    # [x] non delimited text nodes retain type of TEXT
    # [x] ` delimiter maps to type of CODE
    # [x] ** delimiter maps to type of BOLD
    # [x] * delimiter maps to type of ITALIC
    # [-] *** delimeter maps to type of BOLD_ITALIC
    # [?] processes a list of nodes with different delimitiers
    
    def test_split_nodes_creates_node_from_delimiter(self):
        old_nodes = [
            TextNode("This is text with a `code block` word in it", TextType.TEXT)
        ]
        result = split_nodes_delimeter(old_nodes, "`", TextType.CODE)    
        expected_nodes = [
            TextNode(text="This is text with a ", text_type=TextType.TEXT),
            TextNode(text="code block", text_type=TextType.CODE),
            TextNode(text=" word in it", text_type=TextType.TEXT)
        ]
        self.assertListEqual(expected_nodes, result)
    
    def test_split_nodes_creates_new_node_from_text_type(self):
        old_nodes = [
            TextNode("`I am a code block`", TextType.TEXT)
        ]
        result = split_nodes_delimeter(old_nodes, "`", TextType.CODE)
        expected_nodes = [
            TextNode(text="I am a code block", text_type=TextType.CODE)
        ]
        self.assertListEqual(expected_nodes, result)
      
    def test_split_nodes_maps_backtick_to_text_type_code(self):
        old_nodes = [
            TextNode("`I am a code block`", TextType.TEXT)
        ]
        result = split_nodes_delimeter(old_nodes, "`", TextType.CODE)
        expected_nodes = [
            TextNode(text="I am a code block", text_type=TextType.CODE)
        ]
        self.assertListEqual(expected_nodes, result)
    
    def test_split_nodes_maps_double_asterisk_to_text_type_bold(self):
        old_nodes = [
            TextNode("I am some text with **some important text** in it", TextType.TEXT)
        ]
        result = split_nodes_delimeter(old_nodes, "**", TextType.BOLD)
        expected_nodes = [
            TextNode(text="I am some text with ", text_type=TextType.TEXT),
            TextNode(text="some important text", text_type=TextType.BOLD),
            TextNode(text=" in it", text_type=TextType.TEXT)
        ]
        self.assertListEqual(expected_nodes, result)
    
    def test_split_nodes_maps_single_asterisk_to_text_type_italic(self):
        old_nodes = [
            TextNode("I am some text with *some emphasized text* in it", TextType.TEXT)
        ]
        result = split_nodes_delimeter(old_nodes, "*", TextType.ITALIC)
        expected_nodes = [
            TextNode(text="I am some text with ", text_type=TextType.TEXT),
            TextNode(text="some emphasized text", text_type=TextType.ITALIC),
            TextNode(text=" in it", text_type=TextType.TEXT)
        ]
        self.assertListEqual(expected_nodes, result)
    
    def text_split_nodes_maps_triple_asterisk_to_text_type_bold_italic(self):
        old_nodes = [
            TextNode("I am some text with ***some emphasized text*** in it", TextType.TEXT)
        ]
        result = split_nodes_delimeter(old_nodes, "***", TextType.BOLD_ITALIC)
        expected_nodes = [
            TextNode(text="I am some text with ", text_type=TextType.TEXT),
            TextNode(text="some emphasized text", text_type=TextType.BOLD_ITALIC),
            TextNode(text=" in it", text_type=TextType.TEXT)
        ]
        self.assertListEqual(expected_nodes, result)

    def test_split_nodes_will_process_multiple_text_nodes(self):
        processed_nodes = []
        starting_nodes = [
            TextNode("I am some text with a `code block` in it and some **bold** text", TextType.TEXT),
            TextNode("I am some text with **some important text** in it", TextType.TEXT),
            TextNode("I am some text with *some emphasized text* and some **bold** text in it", TextType.TEXT),
            TextNode("I am some text with ***some emphasized text***  text in it", TextType.TEXT)
        ]
        delimiters = ["`", "***", "**", "*"]
        new_text_type = TextType.TEXT
        init_list = True
        # for each delimiter, process starting nodes
        for item in delimiters:
            match(item):
                case "`":
                    new_text_type = TextType.CODE
                case "***":
                    new_text_type = TextType.BOLD_ITALIC
                case "**":
                    new_text_type = TextType.BOLD
                case "*":
                    new_text_type = TextType.ITALIC
                case _:
                    new_text_type = TextType.TEXT
            if init_list == True:
                processed_nodes = split_nodes_delimeter(starting_nodes,item,new_text_type)
                init_list = False
            else: processed_nodes = split_nodes_delimeter(processed_nodes,item,new_text_type)

        expected_nodes = [
            TextNode("I am some text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" in it and some ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode("text", TextType.TEXT),
            TextNode("I am some text with ", TextType.TEXT),
            TextNode("some important text", TextType.BOLD),
            TextNode(" in it", TextType.TEXT),
            TextNode("I am some text with ", TextType.TEXT),
            TextNode("some emphasized text", TextType.ITALIC),
            TextNode(" and some ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text in it", TextType.TEXT),
            TextNode("I am some text with ", TextType.TEXT),
            TextNode("some emphasized text", TextType.BOLD_ITALIC),
            TextNode(" text in it", TextType.TEXT)
        ]
        self.assertListEqual(expected_nodes, processed_nodes)
       
    # Tests for extract_markdown_images
    def test_extract_markdown_images_will_extract_from_text(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        result = extract_markdown_images(text)
        expected_output = [
            ('rick roll', 'https://i.imgur.com/aKaOqIh.gif', ''), 
            ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg', '')]
        self.assertListEqual(expected_output, result)
        
    # Tests for extract_markdown_links
    def test_extract_markdown_images_will_extract_from_text(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        result = extract_markdown_links(text)
        expected_output = [
            ('to boot dev', 'https://www.boot.dev', ''), 
            ('to youtube', 'https://www.youtube.com/@bootdotdev', '')
        ]
        self.assertListEqual(expected_output, result)
    
    # Tests for split_nodes_image
    
    # [-] ignores IMAGE, CODE, ITALIC, BOLD AND LINK nodes
    # [-] will convert a list of "TEXT" type nodes
    # [-] will process a list of varied TextNodes
    # [?] will preserve order of processed nodes
    def test_extract_image_ignores_image_nodes(self):
        images_nodes_list = [
            TextNode(text = "rick roll", url="https://i.imgur.com/aKaOqIh.gif", text_type=TextType.IMAGE),
            TextNode(text = "obi wan", url="https://i.imgur.com/fJRm4Vk.jpeg", text_type=TextType.IMAGE),
            TextNode(text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)", text_type=TextType.TEXT)
        ]
        result = split_nodes_image(images_nodes_list)
        expected_nodes = [
            TextNode(text = "rick roll", url="https://i.imgur.com/aKaOqIh.gif", text_type=TextType.IMAGE),
            TextNode(text = "obi wan", url="https://i.imgur.com/fJRm4Vk.jpeg", text_type=TextType.IMAGE),
            TextNode(text = "This is text with a ", text_type=TextType.TEXT),
            TextNode(text = "rick roll", url = "https://i.imgur.com/aKaOqIh.gif", text_type=TextType.IMAGE)
        ]
        self.assertListEqual(expected_nodes, result)
    
    def test_extract_image_ignores_code_nodes(self):
        images_nodes_list = [
            TextNode(text = "`my awesome code snippet`", text_type=TextType.CODE),
            TextNode(text = "`an even better code snippet`", text_type=TextType.CODE),
            TextNode(text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)", text_type=TextType.TEXT)
        ]
        result = split_nodes_image(images_nodes_list)
        expected_nodes = [
            TextNode(text = "`my awesome code snippet`", text_type=TextType.CODE),
            TextNode(text = "`an even better code snippet`", text_type=TextType.CODE),
            TextNode(text = "This is text with a ", text_type=TextType.TEXT),
            TextNode(text = "rick roll", url = "https://i.imgur.com/aKaOqIh.gif", text_type=TextType.IMAGE)
        ]
        self.assertListEqual(expected_nodes, result)
    
    def test_extract_image_ignores_italic_nodes(self):
        images_nodes_list = [
            TextNode(text = "*my awesome italic text*", text_type=TextType.ITALIC),
            TextNode(text = "*something very profound*", text_type=TextType.ITALIC),
            TextNode(text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)", text_type=TextType.TEXT)
        ]
        result = split_nodes_image(images_nodes_list)
        expected_nodes = [
            TextNode(text = "*my awesome italic text*", text_type=TextType.ITALIC),
            TextNode(text = "*something very profound*", text_type=TextType.ITALIC),
            TextNode(text = "This is text with a ", text_type=TextType.TEXT),
            TextNode(text = "rick roll", url = "https://i.imgur.com/aKaOqIh.gif", text_type=TextType.IMAGE)
        ]
        self.assertListEqual(expected_nodes, result)
    
    def test_extract_image_ignores_bold_nodes(self):
        images_nodes_list = [
            TextNode(text = "**my awesome italic text**", text_type=TextType.BOLD),
            TextNode(text = "**something very profound**", text_type=TextType.BOLD),
            TextNode(text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)", text_type=TextType.TEXT)
        ]
        result = split_nodes_image(images_nodes_list)
        expected_nodes = [
            TextNode(text = "**my awesome italic text**", text_type=TextType.BOLD),
            TextNode(text = "**something very profound**", text_type=TextType.BOLD),
            TextNode(text = "This is text with a ", text_type=TextType.TEXT),
            TextNode(text = "rick roll", url = "https://i.imgur.com/aKaOqIh.gif", text_type=TextType.IMAGE)
        ]
        self.assertListEqual(expected_nodes, result)
    
    def test_extract_image_ignores_link_nodes(self):
        images_nodes_list = [
            TextNode(text = "This is text with a link [to boot dev](https://www.boot.dev)", text_type=TextType.LINK),
            TextNode(text = "This is a youtube link -> [to youtube](https://www.youtube.com/@bootdotdev)", text_type=TextType.LINK),
            TextNode(text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)", text_type=TextType.TEXT)
        ]
        result = split_nodes_image(images_nodes_list)
        expected_nodes = [
            TextNode(text = "This is text with a link [to boot dev](https://www.boot.dev)", text_type=TextType.LINK),
            TextNode(text = "This is a youtube link -> [to youtube](https://www.youtube.com/@bootdotdev)", text_type=TextType.LINK),
            TextNode(text = "This is text with a ", text_type=TextType.TEXT),
            TextNode(text = "rick roll", url = "https://i.imgur.com/aKaOqIh.gif", text_type=TextType.IMAGE)
        ]
        self.assertListEqual(expected_nodes, result)
    
    def test_extract_image_converts_text_type_nodes_list(self):
        images_nodes_list = [
            TextNode(text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)", text_type=TextType.TEXT),
            TextNode(text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)", text_type=TextType.TEXT),
            TextNode(text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)", text_type=TextType.TEXT),
            TextNode(text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)", text_type=TextType.TEXT)
        ]
        result = split_nodes_image(images_nodes_list)
        expected_nodes = [
            TextNode(text = "This is text with a ", text_type=TextType.TEXT),
            TextNode(text = "rick roll", url = "https://i.imgur.com/aKaOqIh.gif", text_type=TextType.IMAGE),
            TextNode(text = "This is text with a ", text_type=TextType.TEXT),
            TextNode(text = "rick roll", url = "https://i.imgur.com/aKaOqIh.gif", text_type=TextType.IMAGE),
            TextNode(text = "This is text with a ", text_type=TextType.TEXT),
            TextNode(text = "rick roll", url = "https://i.imgur.com/aKaOqIh.gif", text_type=TextType.IMAGE),   
            TextNode(text = "This is text with a ", text_type=TextType.TEXT),
            TextNode(text = "rick roll", url = "https://i.imgur.com/aKaOqIh.gif", text_type=TextType.IMAGE)
        ]
        self.assertListEqual(expected_nodes, result)
    
    def test_extract_image_converts_varied_text_type_nodes_list(self):
        images_nodes_list = [
            TextNode(text = "rick roll", url="https://i.imgur.com/aKaOqIh.gif", text_type=TextType.IMAGE),
            TextNode(text = "This is text with a link [to boot dev](https://www.boot.dev)", text_type=TextType.LINK),
            TextNode(text = "**my awesome italic text**", text_type=TextType.BOLD),
            TextNode(text = "`my awesome code snippet`", text_type=TextType.CODE),
            TextNode(text = "*my awesome italic text*", text_type=TextType.ITALIC),    
            TextNode(text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)", text_type=TextType.TEXT)
        ]
        result = split_nodes_image(images_nodes_list)
        expected_nodes = [
            TextNode(text = "rick roll", url="https://i.imgur.com/aKaOqIh.gif", text_type=TextType.IMAGE),
            TextNode(text = "This is text with a link [to boot dev](https://www.boot.dev)", text_type=TextType.LINK),
            TextNode(text = "**my awesome italic text**", text_type=TextType.BOLD),
            TextNode(text = "`my awesome code snippet`", text_type=TextType.CODE),
            TextNode(text = "*my awesome italic text*", text_type=TextType.ITALIC),    
            TextNode(text = "This is text with a ", text_type=TextType.TEXT),
            TextNode(text = "rick roll", url = "https://i.imgur.com/aKaOqIh.gif", text_type=TextType.IMAGE)
        ]
        self.assertListEqual(expected_nodes, result)
    
    # Tests for split_nodes_link
    
    # [-] ignores IMAGE, CODE, ITALIC, BOLD AND LINK nodes
    # [-] will convert a list of "TEXT" type nodes
    # [-] will process a list of varied TextNodes
    # [?] will preserve order of processed nodes
    
    def test_extract_link_ignores_image_nodes(self):
        links_nodes_list = [
            TextNode(text = "rick roll", url="https://i.imgur.com/aKaOqIh.gif", text_type=TextType.IMAGE),
            TextNode(text = "obi wan", url="https://i.imgur.com/fJRm4Vk.jpeg", text_type=TextType.IMAGE),
            TextNode(text = "This is text with a link [to boot dev](https://www.boot.dev)", text_type=TextType.TEXT)
        ]
        result = split_nodes_link(links_nodes_list)
        expected_nodes = [
            TextNode(text = "rick roll", url="https://i.imgur.com/aKaOqIh.gif", text_type=TextType.IMAGE),
            TextNode(text = "obi wan", url="https://i.imgur.com/fJRm4Vk.jpeg", text_type=TextType.IMAGE),
            TextNode(text = "This is text with a link ", text_type=TextType.TEXT),
            TextNode(text = "to boot dev", url = "https://www.boot.dev", text_type=TextType.LINK)
        ]
        self.assertListEqual(expected_nodes, result)
    
    def test_extract_link_ignores_code_nodes(self):
        links_nodes_list = [
            TextNode(text = "`my awesome code snippet`", text_type=TextType.CODE),
            TextNode(text = "`an even better code snippet`", text_type=TextType.CODE),
            TextNode(text = "This is text with a link [to boot dev](https://www.boot.dev)", text_type=TextType.TEXT)
        ]
        result = split_nodes_link(links_nodes_list)
        expected_nodes = [
            TextNode(text = "`my awesome code snippet`", text_type=TextType.CODE),
            TextNode(text = "`an even better code snippet`", text_type=TextType.CODE),
            TextNode(text = "This is text with a link ", text_type=TextType.TEXT),
            TextNode(text = "to boot dev", url = "https://www.boot.dev", text_type=TextType.LINK)
        ]
        self.assertListEqual(expected_nodes, result)
    
    def test_extract_link_ignores_italic_nodes(self):
        links_nodes_list = [
            TextNode(text = "*my awesome italic text*", text_type=TextType.ITALIC),
            TextNode(text = "*something very profound*", text_type=TextType.ITALIC),
            TextNode(text = "This is text with a link [to boot dev](https://www.boot.dev)", text_type=TextType.TEXT)
        ]
        result = split_nodes_link(links_nodes_list)
        expected_nodes = [
            TextNode(text = "*my awesome italic text*", text_type=TextType.ITALIC),
            TextNode(text = "*something very profound*", text_type=TextType.ITALIC),
            TextNode(text = "This is text with a link ", text_type=TextType.TEXT),
            TextNode(text = "to boot dev", url = "https://www.boot.dev", text_type=TextType.LINK)
        ]
        self.assertListEqual(expected_nodes, result)
    
    def test_extract_link_ignores_bold_nodes(self):
        links_nodes_list = [
            TextNode(text = "**my awesome italic text**", text_type=TextType.BOLD),
            TextNode(text = "**something very profound**", text_type=TextType.BOLD),
            TextNode(text = "This is text with a link [to boot dev](https://www.boot.dev)", text_type=TextType.TEXT)
        ]
        result = split_nodes_link(links_nodes_list)
        expected_nodes = [
            TextNode(text = "**my awesome italic text**", text_type=TextType.BOLD),
            TextNode(text = "**something very profound**", text_type=TextType.BOLD),
            TextNode(text = "This is text with a link ", text_type=TextType.TEXT),
            TextNode(text = "to boot dev", url = "https://www.boot.dev", text_type=TextType.LINK)
        ]
        self.assertListEqual(expected_nodes, result)
    
    def test_extract_link_ignores_link_nodes(self):
        links_nodes_list = [
            TextNode(text = "This is text with a link [to boot dev](https://www.boot.dev)", text_type=TextType.LINK),
            TextNode(text = "This is a youtube link -> [to youtube](https://www.youtube.com/@bootdotdev)", text_type=TextType.LINK),
            TextNode(text = "This is text with a link [to boot dev](https://www.boot.dev)", text_type=TextType.TEXT)
        ]
        result = split_nodes_link(links_nodes_list)
        expected_nodes = [
            TextNode(text = "This is text with a link [to boot dev](https://www.boot.dev)", text_type=TextType.LINK),
            TextNode(text = "This is a youtube link -> [to youtube](https://www.youtube.com/@bootdotdev)", text_type=TextType.LINK),
            TextNode(text = "This is text with a link ", text_type=TextType.TEXT),
            TextNode(text = "to boot dev", url = "https://www.boot.dev", text_type=TextType.LINK)
        ]
        self.assertListEqual(expected_nodes, result)
    
    def test_extract_link_converts_text_type_nodes_list(self):
        links_nodes_list = [
            TextNode(text = "This is text with a link [to boot dev](https://www.boot.dev)", text_type=TextType.TEXT),
            TextNode(text = "This is text with a link [to boot dev](https://www.boot.dev)", text_type=TextType.TEXT),
            TextNode(text = "This is text with a link [to boot dev](https://www.boot.dev)", text_type=TextType.TEXT),
            TextNode(text = "This is text with a link [to boot dev](https://www.boot.dev)", text_type=TextType.TEXT)
        ]
        result = split_nodes_link(links_nodes_list)
        expected_nodes = [
            TextNode(text = "This is text with a link ", text_type=TextType.TEXT),
            TextNode(text = "to boot dev", url = "https://www.boot.dev", text_type=TextType.LINK),
            TextNode(text = "This is text with a link ", text_type=TextType.TEXT),
            TextNode(text = "to boot dev", url = "https://www.boot.dev", text_type=TextType.LINK),
            TextNode(text = "This is text with a link ", text_type=TextType.TEXT),
            TextNode(text = "to boot dev", url = "https://www.boot.dev", text_type=TextType.LINK),
            TextNode(text = "This is text with a link ", text_type=TextType.TEXT),
            TextNode(text = "to boot dev", url = "https://www.boot.dev", text_type=TextType.LINK)
        ]
        self.assertListEqual(expected_nodes, result)
    
    def test_extract_link_converts_varied_text_type_nodes_list(self):
        links_nodes_list = [
            TextNode(text = "rick roll", url="https://i.imgur.com/aKaOqIh.gif", text_type=TextType.IMAGE),
            TextNode(text = "This is text with a link [to boot dev](https://www.boot.dev)", text_type=TextType.LINK),
            TextNode(text = "**my awesome italic text**", text_type=TextType.BOLD),
            TextNode(text = "`my awesome code snippet`", text_type=TextType.CODE),
            TextNode(text = "*my awesome italic text*", text_type=TextType.ITALIC),    
            TextNode(text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)", text_type=TextType.TEXT),
            TextNode(text = "This is text with a link [to boot dev](https://www.boot.dev)", text_type=TextType.TEXT)
        ]
        result = split_nodes_link(links_nodes_list)
        expected_nodes = [
            TextNode(text = "rick roll", url="https://i.imgur.com/aKaOqIh.gif", text_type=TextType.IMAGE),
            TextNode(text = "This is text with a link [to boot dev](https://www.boot.dev)", text_type=TextType.LINK),
            TextNode(text = "**my awesome italic text**", text_type=TextType.BOLD),
            TextNode(text = "`my awesome code snippet`", text_type=TextType.CODE),
            TextNode(text = "*my awesome italic text*", text_type=TextType.ITALIC),    
            TextNode(text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)", text_type=TextType.TEXT),
            TextNode(text = "This is text with a link ", text_type=TextType.TEXT),
            TextNode(text = "to boot dev", url = "https://www.boot.dev", text_type=TextType.LINK)
        ]
        self.assertListEqual(expected_nodes, result)
        
    # Tests for text_to_textnodes
    
    def test_text_to_textnodes_converts_md_string(self):
        text_string = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_textnodes(text_string)
        expected_output = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev")
        ]
        self.assertListEqual(expected_output, result)
        
    def test_text_to_textnodes_handles_empty_string(self):
        text_string = ""
        result = text_to_textnodes(text_string)
        expected_output = []
        self.assertListEqual(expected_output, result)

    def test_text_to_textnodes_handles_repeating_patterns(self):
        text_string = "**text** **text** **text** **text** **text** **text**"
        result = text_to_textnodes(text_string)
        expected_output = [
            TextNode("text", TextType.BOLD),
            TextNode("text", TextType.BOLD),
            TextNode("text", TextType.BOLD),
            TextNode("text", TextType.BOLD),
            TextNode("text", TextType.BOLD),
            TextNode("text", TextType.BOLD)
        ]
        self.assertListEqual(expected_output, result)
    
    def test_text_to_textnodes_handles_embedded_patterns(self):
        text_string = "this is some embedded text **super bold with *emphasized* text in it**. what do you think?"
        result = text_to_textnodes(text_string)
        expected_output = [
            TextNode("this is some embedded text ", TextType.TEXT),
            TextNode("super bold with ", TextType.BOLD),
            TextNode("emphasized", TextType.ITALIC),
            TextNode(" text in it", TextType.BOLD),
            TextNode(". what do you think?", TextType.TEXT),
        ]
        self.assertListEqual(expected_output, result)
    
    # Tests for markdown_to_blocks

    # [-] will remove excessive new lines
    # [-] will split paragraphs on \n\n
    # [-] will remove trailing and leading whitespaces
    
    def test_markdown_to_blocks_removes_excessive_new_lines(self):
        md = """# This is a heading



This is a paragraph of text. It has some **bold** and *italic* words inside of it.




* This is the first list item in a list block
* This is a list item
* This is another list item"""
        result = markdown_to_blocks(md)
        expected = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
        ]
        self.assertListEqual(expected, result)
   
    def text_markdown_to_blocks_splits_paragraphs_on_double_newline_char(self):
        md = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"""
        result = markdown_to_blocks(md)
        expected = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
        ]
        self.assertListEqual(expected, result)
 
    def test_markdown_to_blocks_removes_leading_and_trailing_whitespace(self):
        md = """ # This is a heading 

 This is a paragraph of text. It has some **bold** and *italic* words inside of it. 

 * This is the first list item in a list block 
 * This is a list item 
 * This is another list item """
        result = markdown_to_blocks(md)
        expected = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
        ]
        self.assertListEqual(expected, result)

    # Tests for block_to_block_type
    
    # [-] UL -> asterisk
    # [-] UL -> Hypen
    # [-] code
    # [-] quote
    # [-] OL
    # [-] Paragraph
    
    def test_block_to_block_type_ul_asterisk(self):
        text = """* This is the first list item in a list block
* This is a list item
* This is another list item"""
        result = block_to_block_type(text)
        expected = "unordered_list"
        self.assertEqual(expected, result)
    
    def test_block_to_block_type_ul_hyphen(self):
        text = """- This is the first list item in a list block
- This is a list item
- This is another list item"""
        result = block_to_block_type(text)
        expected = "unordered_list"
        self.assertEqual(expected, result)
    
    def test_block_to_block_type_code(self):
        text = """```This is my spectacular code block in C++. I hope you
    appreciate its magnificence.```"""
        result = block_to_block_type(text)
        expected = "code"
        self.assertEqual(expected, result)
    
    def test_block_to_block_type_quote(self):
        text = """> This is simply the best
> quote you are going to hear in your lifetime
> so I hope you have a pen and paper handy to make
> some life changing notes.
> -- Fujivato, 2024
"""
        result = block_to_block_type(text)
        expected = "quote"
        self.assertEqual(expected, result)
    
    def test_block_to_block_type_ol_when_numbers_contiguous(self):
        text = """1. most important item
2. second most important item
3. third most important item
4. fourth most important item
5. fifth most important item

"""
        result = block_to_block_type(text)
        expected = "ordered_list"
        self.assertEqual(expected, result)
    
    def test_block_to_block_type_paragraph_when_numbers_not_contiguous(self):
        text = """2. second most important item
1. first most important item
4. fourth most important item
3. third most important item
6. sixth most important item
5. fifth most important item
"""
        result = block_to_block_type(text)
        expected = "paragraph"
        self.assertEqual(expected, result)
    
    def test_block_to_block_type_default(self):
        text = """This is some non-specific markdown text in a block that we 
will be treating as a paragraph of text i.e. the default option.
"""
        result = block_to_block_type(text)
        expected = "paragraph"
        self.assertEqual(expected, result)
    
    # Tests for markdown_to_html_node
    
    # Tests for markdown_block_to_html_blockquote
    
    # Tests for markdown_block_to_html_headings
    
    # Tests for markdown_block_to_html_code_block
    
    # Tests for markdown_block_to_html_ordered_list
    
    # Tests for markdown_block_to_html_unordered_list
    
    # Tests for text_to_children
    
if __name__ == "__main__":
    unittest.main()
