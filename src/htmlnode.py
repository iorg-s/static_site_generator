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