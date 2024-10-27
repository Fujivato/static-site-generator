import re
from src.leafnode import LeafNode
from src.textnode import TextType, TextNode
from src.blocktype import BlockType

def text_node_to_html_node(text_node):
    match(text_node.text_type):
        case TextType.TEXT:
            return LeafNode(value=text_node.text)
        case TextType.BOLD:
            return LeafNode("b", value=text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", value=text_node.text)
        case TextType.CODE:
            return LeafNode("code", value=text_node.text)
        case TextType.LINK:
            return LeafNode("a", value=text_node.text, props={ "href": text_node.url })
        case TextType.IMAGE:
            return LeafNode("img", value="", props={ "src": text_node.url, "alt": text_node.text })
        case _:
            raise Exception("Unknown TextNode type")
        
def split_nodes_delimeter(old_nodes, delimiter, text_type):
    new_nodes = []
    new_text_type = text_type

    for node in old_nodes:

        if isinstance(node, TextNode) and (node.text_type == TextType.TEXT or node.text_type == TextType.BOLD or node.text_type == TextType.ITALIC or node.text_type == TextType.CODE):
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

def extract_markdown_images(text):
    return re.findall(r"(?:[!]\[(?P<caption>.*?)\])\((?P<image>.*?)(?P<description>\".*?\")?\)",text)
    
def extract_markdown_links(text):
    return re.findall(r"(?:\[(?P<caption>.*?)\])\((?P<image>.*?)(?P<description>\".*?\")?\)",text)

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

def text_to_textnodes(text):
    if text == "": return []
    
    text_node = TextNode(text = f"{text}", text_type = TextType.TEXT)
    node_list = [text_node]
    
    # convert text level items to TextNodex
    delimiter_list = ["**", "*", "`"]
    for symbol in delimiter_list:
        node_text_type = TextType.TEXT
        match(symbol):
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
        raw_blocks[i]  = '\n'.join(inner_items)
        
    return raw_blocks

def block_to_block_type(md_block):
    # conditions:
    
    # 1. detect headings # 1-6
    regex_heading = "^([#]{1,6})[\s,\w,\d]+$"
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
        if item[0:1] == "*" or item[0:1] == "-": ul_block.append((item, True))
        else: ul_block.append((item, False))
        
        # 5. ordered list block
        prefix = item.split(" ")[0] # e.g. 1.
        cardinal_number = prefix.replace(".", "").strip()
        try:
            ol_block.append((int(cardinal_number), prefix, item))    
        except ValueError:
            continue
    
    is_quote_block = list(filter(lambda x: x[1] == False, quote_block))
    is_ul_block = list(filter(lambda x: x[1] == False, ul_block))
    ol_compare = [] 
    
    for i in range(1, len(ol_block) + 1):
        ol_compare.append(i)
    
    ol_block_cardinals = list(map(lambda x: x[0], ol_block))
    ol_block_contiguous = len(ol_block_cardinals) > 0 and ol_compare == ol_block_cardinals

    if len(is_quote_block) == 0: return BlockType.QUOTE.value
    if len(is_ul_block) == 0: return BlockType.UNORDERED_LIST.value
    if ol_block_contiguous == True: return BlockType.ORDERED_LIST.value
    
    # if none of the above conditions are met, block is a normal paragraph
    return BlockType.PARAGRAPH.value
    
def markdown_to_html_node(markdown):
    pass