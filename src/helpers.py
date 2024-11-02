import re
import os
import shutil
from src.leafnode import LeafNode
from src.textnode import TextType, TextNode
from src.parentnode import ParentNode
from src.blocktype import BlockType

# accepts a TextNode and returns a LeafNode (HTMLNode) 
def text_node_to_html_node(text_node):
    match(text_node.text_type):
        case TextType.TEXT:
            return LeafNode(value=text_node.text)
        case TextType.BOLD:
            return LeafNode("b", value=text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", value=text_node.text)
        case TextType.BOLD_ITALIC:
            return LeafNode("bi", value=text_node.text)
        case TextType.CODE:
            return LeafNode("code", value=text_node.text)
        case TextType.LINK:
            return LeafNode("a", value=text_node.text, props={ "href": text_node.url })
        case TextType.IMAGE:
            return LeafNode("img", value="", props={ "src": text_node.url, "alt": text_node.text })
        case _:
            raise Exception("Unknown TextNode type")

# accepts a list of TextNodes with type "TEXT", "CODE", "BOLD", "ITALIC"
# and returns a list of split TextNodes with adjusted text_type   
def split_nodes_delimeter(old_nodes, delimiter, text_type):
    new_nodes = []
    new_text_type = text_type

    for node in old_nodes:

        if isinstance(node, TextNode) and (node.text_type == TextType.TEXT or node.text_type == TextType.BOLD or node.text_type == TextType.ITALIC or node.text_type == TextType.BOLD_ITALIC or node.text_type == TextType.CODE):
            node.text = node.text.replace(delimiter, f"||{delimiter}||")
            string_list = node.text.split(delimiter)

            for text_string in string_list:
                if text_string[ :2] == "||" and text_string[len(text_string)-2:] == "||": 
                    new_text = text_string.replace("||","").strip()
                    if new_text != "": new_nodes.append(TextNode(text=f"{new_text}", text_type=new_text_type))
                else: 
                    new_text = text_string.replace("||","")
                    if new_text != "": new_nodes.append(TextNode(text=f"{new_text}", text_type=node.text_type))                          
                    
        else: new_nodes.append(node)
        
    return new_nodes

# regex to match snippets of markdown text containing an image definition
def extract_markdown_images(text):
    return re.findall(r"(?:[!]\[(?P<caption>.*?)\])\((?P<image>.*?)(?P<description>\".*?\")?\)",text)
 
 # regex to match snippets of markdown text containing a link definition   
def extract_markdown_links(text):
    return re.findall(r"(?:\[(?P<caption>.*?)\])\((?P<image>.*?)(?P<description>\".*?\")?\)",text)

# accepts a list of TextNodes with type "TEXT"
# returns a list of split TextNodes with type "IMAGE"
def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if isinstance(node, TextNode) and node.text_type == TextType.TEXT:
            image_links = extract_markdown_images(node.text)

            for i in range(0,len(image_links)):
                query = f"![{image_links[i][0]}]({image_links[i][1]})"
                node.text = node.text.replace(query, f"|{i}|")
            
            split_elements = node.text.split('|')

            for element in split_elements:
                try:
                    index = int(element)
                    if index < len(split_elements):
                        new_nodes.append(TextNode(text=f"{image_links[index][0]}", url=f"{image_links[index][1]}", text_type=TextType.IMAGE))
                    else: new_nodes.append(TextNode(text=f"{element}", text_type=node.text_type))       
                    continue 
                except ValueError:
                    pass
                if element.strip() != "": new_nodes.append(TextNode(text=f"{element}", text_type=node.text_type))
        else: new_nodes.append(node)
    
    return new_nodes

# accepts a list of TextNodes with type "TEXT"
# returns a list of split TextNodes with type "LINK"
def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if isinstance(node, TextNode) and node.text_type == TextType.TEXT:
            img_links = extract_markdown_images(node.text)
            url_links = extract_markdown_links(node.text)

            for i in range(0,len(url_links)):
                query = f"[{url_links[i][0]}]({url_links[i][1]})"
                
                if len(img_links) == 0 or (url_links[i][0] not in list(img_links[0]) and url_links[i][1] not in list(img_links[1])):
                    node.text = node.text.replace(query, f"|{i}|")
            
            split_elements = node.text.split('|')

            for element in split_elements:
                try:
                    index = int(element)
                    if index < len(split_elements):
                        new_nodes.append(TextNode(text=f"{url_links[index][0]}", url=f"{url_links[index][1]}", text_type=TextType.LINK))
                    else: new_nodes.append(TextNode(text=f"{element}", text_type=node.text_type))       
                    continue 
                except ValueError:
                    pass
                if element.strip() != "": new_nodes.append(TextNode(text=f"{element}", text_type=node.text_type))
        else: new_nodes.append(node)
    
    return new_nodes

# accepts a string of markdown text and
# returns a list of TextNodes with respective text_type
def text_to_textnodes(text):
    if text == "": return []
       
    text_node = TextNode(text = f"{text}", text_type = TextType.TEXT)
    node_list = [text_node]

    # convert text level items to TextNodex
    delimiter_list = ["***", "**", "*", "`"]
    for symbol in delimiter_list:
        node_text_type = TextType.TEXT
        match(symbol):
            case "***":
                node_text_type = TextType.BOLD_ITALIC
            case "**":
                node_text_type = TextType.BOLD
            case "*":
                node_text_type = TextType.ITALIC
            case "`":
                node_text_type = TextType.CODE
            case _:
                node_text_type = TextType.TEXT            
        node_list = split_nodes_delimeter(node_list, symbol, node_text_type)
    
    # extract images
    node_list = split_nodes_image(node_list)
    
    # extract links
    node_list = split_nodes_link(node_list)
    
    return node_list

# accepts a string of markdown text and returns
# a list of "markdowm" blocks ready for processing
def markdown_to_blocks(markdown):
    raw_blocks = markdown.split('\n\n')

    # remove any empty or newline entries
    for item in raw_blocks:
        if item == "" or item == '\n':
            raw_blocks.remove(item)

    # remove any leading or trailing whitespace:
    for i in range(0, len(raw_blocks)):
        raw_blocks[i] = raw_blocks[i].strip()
        inner_items = raw_blocks[i].split('\n')
        for j in range(0, len(inner_items)):
            inner_items[j] = inner_items[j].strip()
        raw_blocks[i]  = '\n'.join(inner_items).strip()

    return raw_blocks

# accepts a list of "markdown" blocks and assigns them to a
# supported BlockType enum
def block_to_block_type(md_block):
    # conditions:

    # 1. detect headings # 1-6
    regex_heading = "^([#]{1,6})([ ]{1})(.)+"
    is_heading = re.findall(regex_heading, md_block)
    if len(is_heading) > 0: return BlockType.HEADING.value
    
    # 2. code blocks must start and end with 3 backticks
    first_3_characters = md_block[:3]
    last_3_characters = md_block[-3:] 
    
    if first_3_characters.strip() == "```" and last_3_characters.strip() == "```":
        return BlockType.CODE.value

    block_lines = md_block.split('\n')
    # 3. every line in a quote must begin with >
    # 4. everyline in an unordered block must start with a * or - character
    # 5. every line in an ordered block must start with a number followed by . and be contiguous
    
    quote_block = []
    ul_block = []
    ol_block = []
    
    for item in block_lines:
        if item.strip() == "": continue
        
        # 3. quote block
        if item[0:1] == ">": quote_block.append((item, True))
        else: quote_block.append((item, False))

        # 4. unordered list block
        # 1 space for top level list, 3 spaces for nested list
        if item[0:2] == "* " or item[0:2] == "- ": ul_block.append((item, True))
        else: ul_block.append((item, False))
        
        # 5. ordered list block
        prefix = item.split(" ")[0] # e.g. 1.
        cardinal_number = prefix.replace(".", "").strip()
        try:
            ol_block.append((int(cardinal_number), prefix, item))    
        except ValueError:
            continue
    
    is_quote_block = list(filter(lambda x: x[1] == True, quote_block))
    is_ul_block = list(filter(lambda x: x[1] == True, ul_block))
    ol_compare = [] 
    
    for i in range(1, len(ol_block) + 1):
        ol_compare.append(i)
    
    ol_block_cardinals = list(map(lambda x: x[0], ol_block))
    ol_block_contiguous = len(ol_block_cardinals) > 0 and ol_compare == ol_block_cardinals

    if len(is_quote_block) > 0: return BlockType.QUOTE.value
    if len(is_ul_block) > 0: return BlockType.UNORDERED_LIST.value
    if ol_block_contiguous == True: return BlockType.ORDERED_LIST.value
    
    # if none of the above conditions are met, block is a normal paragraph
    return BlockType.PARAGRAPH.value

# Helper functions to accompany this:

# 1. text_to_children
# accepts a string of text and returns a list of HTMLNodes
# that represent inline markdown
def text_to_children(text):
    html_nodes = []
    
    # 2.1 determine the type of block (with existing function)
    block_type = block_to_block_type(text)

    # 2.2 based on type of block, create a new HTMLNode with proper data
    match(block_type): 
        # unordered lists
        case BlockType.UNORDERED_LIST.value:
            html_nodes.append(markdown_block_to_html_unordered_list(text))
        # ordered lists
        case BlockType.ORDERED_LIST.value:
            html_nodes.append(markdown_block_to_html_ordered_list(text))
        # quotes
        case BlockType.QUOTE.value:
            html_nodes.append(markdown_block_to_html_blockquote(text))
        # code blocks
        case BlockType.CODE.value:
            html_nodes.append(markdown_block_to_html_code_block(text))
        # heading blocks
        case BlockType.HEADING.value:
            html_nodes = list(html_nodes + markdown_block_to_html_headings(text))
        # paragraphs
        case _:
            node_list = split_nodes_link(split_nodes_image(text_to_textnodes(text)))
            for node in node_list:
                 html_nodes.append(text_node_to_html_node(node))
                
    return html_nodes

# 2. extract ULs
# accepts a block of markdown text and returns a list of HTMLNodes
# representing an unordered list
def markdown_block_to_html_unordered_list(text):  
    li_children = []
    for line in text.split('\n'):
        node_list = text_to_textnodes(line[1:].strip())
        child_nodes = []
        for node in node_list:
            child_nodes.append(text_node_to_html_node(node))
        li_children.append(ParentNode(tag="li", children=child_nodes))
    return ParentNode(tag="ul", children=li_children)

# 3. extract OLs
# accepts a block of markdown text and returns a list of HTMLNodes
# representing an ordered list
def markdown_block_to_html_ordered_list(text):
    li_children = []
    for line in text.split('\n'):
        child_nodes = []
        if line != "":
            li_prefix = line.split(" ")[0]
            li_text = line.replace(li_prefix,"").strip() 
            node_list = text_to_textnodes(li_text)
            for node in node_list: 
                child_nodes.append(text_node_to_html_node(node))
            li_children.append(ParentNode(tag="li", children=child_nodes))
    return ParentNode(tag="ol", children=li_children)

# 4. extract code blocks
# accepts a block of markdown text and returns a list of HTMLNodes
# representing a code element
def markdown_block_to_html_code_block(text):
    node_list = text_to_textnodes(text.replace("```", "").strip())
    child_nodes = []
    for node in node_list:
        child_nodes.append(text_node_to_html_node(node))
    return ParentNode(tag="code", children=child_nodes)

# 5. extract headings
# accepts a block of markdown text and returns a list of HTMLNodes
# representing a heading element
def markdown_block_to_html_headings(text):
    html_nodes = []
    for line in text.split('\n'):
        heading_size = line.count("#")
        heading_text = line.replace("#", "").strip()  
        child_nodes = []
        node_list = text_to_textnodes(heading_text)
        for node in node_list:
            child_nodes.append(text_node_to_html_node(node))
        parent_node = ParentNode(tag=f"h{heading_size}", children=child_nodes)
        html_nodes.append(parent_node)
    return html_nodes

# 6. extract quote blocks
# accepts a block of markdown text and returns a list of HTMLNodes
# representing a blockquote element
def markdown_block_to_html_blockquote(text):
    html_nodes = []
    for line in text.split('\n'):
        node_list = text_to_textnodes(line.replace(">","").strip())
        for node in node_list:
            html_nodes.append(text_node_to_html_node(node))
    return ParentNode(tag = "blockquote", children=html_nodes)

# convert markdown to html nodes
def markdown_to_html_node(markdown):
    html_nodes = []
  
    # 1. split the markdown into blocks
    md_blocks = markdown_to_blocks(markdown)

    # 2. loop over each block
    for block in md_blocks:        
        html_nodes = html_nodes + text_to_children(block) 
    
    return ParentNode(tag = "div", children=html_nodes)

# extract the markdown main heading to serve as page title
def extract_title(markdown):    
    regex_heading = "^([#]{1})([ ]{1})(.)+$"
    text_lines = markdown.split('\n')
    h1_heading = []
    
    for line in text_lines:
        result = re.findall(regex_heading, line)
        if len(result) > 0:
            h1_heading.append(line)
        
    if len(h1_heading) == 0:
        raise Exception("No H1 heading found")
    return h1_heading[0].replace("#","").strip()

# generate the html content page from markdown
def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    # read markdown from file:
    md_reader = open(from_path)
    markdown = md_reader.read()
    
    template_reader = open(template_path)
    template = template_reader.read()
    
    html_string = markdown_to_html_node(markdown).to_html().replace("  ", " ")
    page_title = extract_title(markdown)
    
    template = template.replace("{{ Title }}", page_title).replace("{{ Content }}", html_string)
    
    with open(f"{dest_path}", "w") as f:
        f.write(template)

# recursively scan the "content" directory and convert markdown pages to html
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    dir_list = os.listdir(dir_path_content)
    
    for object in dir_list:
        object_name = os.path.join(dir_path_content, object)
        dest_object = os.path.join(dest_dir_path, f"{os.path.splitext(os.path.basename(object))[0]}.html")
        dest_dir = os.path.join(dest_dir_path, object)
        
        if os.path.isfile(object_name):
            generate_page(object_name, template_path, dest_object)          
        else: 
            if not os.path.exists(os.path.join(dest_dir_path, object)):
                os.mkdir(os.path.join(dest_dir_path, object))
            generate_pages_recursive(f"{object_name}", template_path, f"{dest_dir}")
