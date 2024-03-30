from functools import reduce

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        html_props = ""
        if self.props is None:
            return html_props
        for k,v in self.props.items():
            html_props += f' {k}="{v}"'
        return html_props
    
    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None) -> None:
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError("value is required for LeafNode")
        if self.tag is None:
            return str(self.value)
        return f"<{self.tag}{super().props_to_html()}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None) -> None:
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("tag is required for ParentNode")
        if self.children is None:
            raise ValueError("children is required for ParentNode")
        return f'<{self.tag}>{"".join([x.to_html() for x in self.children])}</{self.tag}>'