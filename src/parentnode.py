from src.htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(children = children, tag = tag, props = props)

    def to_html(self):
        if self.tag is None or self.tag == "":
            raise ValueError("Parent nodes must have a tag name")
        
        if self.children is None or len(self.children) == 0:
            raise ValueError("Parent nodes must contain child nodes")
        
        # to-do:
        # add functionality for recursively calling the node tree and r
        # print a full HTML string
        html_string = ""
        tag_string = f"{self.tag} {self.props_to_html()}".strip()
        html_string += f"<{tag_string}>"
        
        for child in self.children:         
            html_string += child.to_html()
        
        html_string = html_string.replace("> ",">").replace(" <", "<")
        html_string = html_string.strip() 
        html_string += f"</{self.tag}>"
        
        return html_string    
        