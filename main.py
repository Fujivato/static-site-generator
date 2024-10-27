from src.textnode import TextNode, TextType
from src.htmlnode import HTMLNode
from src.helpers import markdown_to_html_node, block_to_block_type, markdown_to_blocks, text_to_textnodes, split_nodes_link, split_nodes_image, text_node_to_html_node, split_nodes_delimeter, extract_markdown_images, extract_markdown_links

def main():
    #hello_node = TextNode("This is a test node", NodeType.BOLD, "http://www.example.com")
    #print(hello_node)
    #test_props =  test_props = { "data-py-id": "test id attribute", "data-py-name": "test name attribute" }
    #hello_html =  HTMLNode(tag = "div", props = test_props)
    #print(hello_html)
    
    #p_node_1_1 = HTMLNode(value = "paragraph 1 text")
    #p_node_2_1 = HTMLNode(value = "paragraph 2 text")
        
    #p_node_1 = HTMLNode(tag = "p", children=[p_node_1_1])
    #p_node_2 = HTMLNode(tag = "p", children=[p_node_2_1])
    
    #test_child_nodes = [p_node_1, p_node_2]
    #props =  { "data-py-id": "test id attribute", "data-py-name": "test name attribute" }      
    #node = HTMLNode(tag = "div", props=props)
    #print(node.props_to_html())

    #text_node = TextNode(text = "Hello World", text_type = TextType.TEXT)
    #print(text_node)
    #result = text_node_to_html_node(text_node)
    #print(result)
    #old_nodes = [
    #    TextNode(text="hello world", text_type=TextType.IMAGE, url="https://www.sample.com"),
    #    TextNode("This is text with a `code block` word", TextType.TEXT),
    #    TextNode("This is text with a ** bold phrase ** in it", TextType.BOLD)
    #]
    #delimiter = "**"
    #text_type = TextType.BOLD
    #result = split_nodes_delimeter(old_nodes, delimiter, text_type)    
    #print(result)
    #images_text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
    #extract_markdown_images(images_text)
    
    #links_text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    #extract_markdown_links(links_text)
    

    #images_nodes_list = [
    #    TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.TEXT)
    #]
    #result = split_nodes_image(images_nodes_list)
    
    #links_nodes_list = [
    #    TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT)
    #]
    #result = split_nodes_link(links_nodes_list)
    #print(result)
    #links_nodes_list = [
    #        TextNode(text = "rick roll", url="https://i.imgur.com/aKaOqIh.gif", text_type=TextType.IMAGE),
    #        TextNode(text = "This is text with a link [to boot dev](https://www.boot.dev)", text_type=TextType.LINK),
    #        TextNode(text = "**my awesome italic text**", text_type=TextType.BOLD),
    #        TextNode(text = "`my awesome code snippet`", text_type=TextType.CODE),
    #        TextNode(text = "*my awesome italic text*", text_type=TextType.ITALIC),    
    #        TextNode(text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)", text_type=TextType.TEXT),
    #        TextNode(text = "This is text with a link [to boot dev](https://www.boot.dev)", text_type=TextType.TEXT)
    #]
    #result = split_nodes_link(links_nodes_list)
    #print(result)
    
    #text= "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

    #result = text_to_textnodes(text)
    #print(result)
    
    #grr = TextNode(text = "what", text_type = TextType.TEXT)
    #print(grr)
    
    #output = [
    #    TextNode("This is ", TextType.TEXT, "None"), 
    #    TextNode("text", TextType.BOLD, "None"), 
    #    TextNode(" with an ", TextType.TEXT, "None"), 
    #    TextNode("italic", TextType.ITALIC, "None"), 
    #    TextNode(" word and a ", TextType.TEXT, "None"), 
    #    TextNode("code block", TextType.CODE, "None"), 
    #    TextNode(" and an ", TextType.TEXT, "None"), 
    #    TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"), 
    #    TextNode(" and a ", TextType.TEXT, "None"), 
    #    TextNode("link", TextType.LINK, "https://boot.dev")]
    md = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"""

    #result = markdown_to_blocks(md)
    #print(result)
    
    md_text_ul_asterisk = """* This is the first list item in a list block
* This is a list item
* This is another list item"""

    md_text_ul_hyphen = """- This is the first list item in a list block
- This is a list item
- This is another list item"""
    
    md_text_code_block = """```This is my spectacular code block in C++. I hope you
    appreciate its magnificence.
```"""

    md_text_quote_block = """> This is simply the best
> quote you are going to hear in your lifetime
> so I hope you have a pen and paper handy to make
> some life changing notes.
> -- Fujivato, 2024
"""
    
    md_text_ol_block = """1. most important item
2. second most important item
3. third most important item
4. fourth most important item
5. fifth most important item

"""
    
    md_text_default = """This is some non-specific markdown text in a block that we 
will be treating as a paragraph of text i.e. the default option.
"""
    result = block_to_block_type(md_text_default)
    print(result)

    # [x] UL -> asterisk
    # [x] UL -> Hypen
    # [x] code
    # [x] quote
    # [x] OL
    # [x] Paragraph
        
main()
