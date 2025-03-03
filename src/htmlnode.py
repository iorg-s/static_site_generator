class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    

    def __eq__(self, other):
        return self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props

    def to_html(self):
        raise NotImplemented()


    def props_to_html(self):
        if self.props is None:
            return ""
        html_text = []
        for prop in self.props:
            html_text.append(f"{prop}=\"{self.props[prop]}\"")
        return " ".join(html_text)

    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"
    

            
class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        if value is None:
            raise ValueError("Value must be provided")
        super().__init__(tag=tag, value=value,  props=props)
    
    def to_html(self):
        if self.tag == None:
            return self.value 
        if self.props == None:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        return f"<{self.tag} {self.props_to_html()}>{self.value}</{self.tag}>"