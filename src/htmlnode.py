class HTMLNode():
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
        
    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        html_string = ""
        
        if self.props is not None:
            for attr in self.props:
                html_string += f'{attr}="{self.props[attr]}" '
            
        return html_string.strip()
    
    def __generate_node_tree__(self, node, level = 1):
        if node.tag is None: tree_string = "<text>"
        else: tree_string = f"<{node.tag}>"
        
        if node.children is not None and len(node.children) > 0:
            for child in node.children:
                tree_string += "\n" + (" " * level) + " ↳ " + self.__generate_node_tree__(child, level + 1)
        
        return tree_string
 
    def get_node_tree(self):
        node_tree = f"HTML Node Tree for {self.tag}\n"
        node_tree += "======================================\n"
        node_tree += self.__generate_node_tree__(self)
        return node_tree       
           
    def __repr__(self):
        html_string = f"HTMLNode({self.tag}, {self.value})"    
       
        if self.props is not None and len(self.props) > 0:
            html_string += "\n  Props:\n"
            
            for prop in self.props:
                html_string += f'     "{prop}": "{self.props[prop]}"\n'
                
        return html_string