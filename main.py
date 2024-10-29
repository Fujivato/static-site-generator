from src.textnode import TextNode, TextType
from src.htmlnode import HTMLNode
from src.helpers import markdown_to_html_node, text_to_children, markdown_to_html_node, block_to_block_type, markdown_to_blocks, text_to_textnodes, split_nodes_link, split_nodes_image, text_node_to_html_node, split_nodes_delimeter, extract_markdown_images, extract_markdown_links


def main():
    file_name = "example-markdown.md"
    reader = open(file_name)
    md_text = reader.read()
    
    # debug output
    #print(md_text)
    
    #result = markdown_to_html_node(md_text)
    #print(result.get_node_tree())

main()
