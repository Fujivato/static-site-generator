from enum import Enum

class TextType(Enum):
    TEXT = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    BOLD_ITALIC = "bolditalic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():
    def __init__(self, text, text_type, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        text_match = self.text.strip().lower() == other.text.strip().lower()
        type_match = self.text_type == other.text_type
        url_match = None
        
        if self.url is not None:
            url_match = self.url.strip().lower() == other.url.strip().lower()
            return text_match and type_match and (url_match is not None and url_match)
        
        return text_match and type_match
    
    def __repr__(self):
        url_string = None
        if self.url is not None: url_string = f'"{self.url}"'
        return f"""TextNode("{self.text}", {self.text_type}, {url_string})"""
