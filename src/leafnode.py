from src.htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag = None, value = "", props = None):
        super().__init__(value = value, tag = tag, props = props)

    def __eq__(self, other):
        same_tag = self.tag == other.tag
        same_value = self.value == other.value
        same_props = self.props == other.props
        return same_tag and same_value and same_props
     
    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        
        if self.tag is None or self.tag == "":
            return f"{self.value}"
        
        prop_string = f" {self.props_to_html()} "
        if self.tag == "bi": 
            tag_string = f" <b><i {prop_string}".strip()
            return f"{tag_string}>{self.value}</i></b>".strip()
            
        tag_string = f"{self.tag} {prop_string}".strip()
        return f"<{tag_string}>{self.value}</{self.tag}>"
