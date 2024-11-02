from src.htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)
  
    def to_html(self):
        if self.tag is None or self.tag == "":
            raise ValueError("Parent nodes must have a tag name")
        
        if self.children is None or len(self.children) == 0:
            raise ValueError("Parent nodes must contain child nodes")
        
        html_string = ""
        tag_string = f"{self.tag} {self.props_to_html()}".strip()
        html_string += f"<{tag_string}>"
        
        for child in self.children:         
            html_string += f"{child.to_html()}"
        
        html_string = html_string.strip() 
        html_string += f"</{self.tag}>"
        
        return html_string.replace("  ", " ").strip()    
        