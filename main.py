import os
import shutil
from src.textnode import TextNode, TextType
from src.htmlnode import HTMLNode
from src.helpers import markdown_to_html_node, text_to_children, markdown_to_html_node, block_to_block_type, markdown_to_blocks, text_to_textnodes, split_nodes_link, split_nodes_image, text_node_to_html_node, split_nodes_delimeter, extract_markdown_images, extract_markdown_links

def md_load_test():
    file_name = "example-markdown.md"
    reader = open(file_name)
    md_text = reader.read()
    
    # debug output
    #print(md_text)
    
    # convert md document to html node tree
    result = markdown_to_html_node(md_text)
    print(result.get_node_tree())

def copy_directory(source_dir, dest_dir):   
    dir_list = os.listdir(source_dir)
    for object in dir_list:
        if os.path.isfile(f"{source_dir}/{object}"):
            print(f"Copying from: '{source_dir}/{object}' to '{dest_dir}/{object}'")
            shutil.copy(f"{source_dir}/{object}", f"{dest_dir}/{object}") 
        else: 
            if not os.path.exists(f"{dest_dir}/{object}"):
                os.mkdir(f"{dest_dir}/{object}")
            copy_directory(f"{source_dir}/{object}", f"{dest_dir}/{object}")

def copy_assets_to_public_dir():
    print("Processing static assets...")
    
    # working directory paths
    source_dir = "static" # staitc folder in root
    dest_dir = "public" # public folder in root
           
    #   delete all content in the destination dir    
    print("Deleting 'public' folder...")
    if os.path.exists(dest_dir):
       shutil.rmtree(dest_dir)

    # make the public directory    
    os.mkdir(dest_dir)
        
    print("Copying assets to 'public' directory...")
    copy_directory(source_dir, dest_dir)
    print("Finished copying assets.")  

def main():
    # test converting md docs to html node trees
    #md_load_test()
    
    # copy assets from 'static' folder to 'public
    copy_assets_to_public_dir()

main()
