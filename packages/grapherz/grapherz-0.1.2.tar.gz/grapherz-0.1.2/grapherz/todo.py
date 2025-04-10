from enum import Enum
class Side(Enum):
    right = "right"
    left = "right"
    top = "top"
    bottom = "bottom"

class Edge:
    __slots__ = ['fromNode', 'fromSide', 'id','label', 'styleAttributes', 'toNode', 'toSide']

    def __init__(self, 
                 from_node: str, 
                 from_side: Side, 
                 id: str, 
                 style_attributes: dict,
                 label:str,
                 to_node: str, 
                 to_side: Side):
        self.fromNode = from_node
        self.fromSide = from_side.value
        self.id = id
        self.styleAttributes = style_attributes
        self.label = label
        self.toNode = to_node
        self.toSide = to_side.value

    def to_dict(self):
        return {attr: getattr(self, attr) for attr in self.__slots__}

class Node:
    __slots__ = ['height', 'width', 'x', 'y', 'id', 'type','text','styleAttributes']

    def __init__(self, 
                 height: int = 60, 
                 width: int = 260, 
                 x: str = 440, 
                 y: dict = 80, 
                 id: str='1', 
                 type = "text",
                 text: str = "开始",
                 styleAttributes:dict={}):
        self.height = height
        self.width = width
        self.x = x
        self.y = y
        self.id = id
        self.type = type
        self.text = text
        self.styleAttributes = styleAttributes

    def to_dict(self):
        return {attr: getattr(self, attr) for attr in self.__slots__}

import json

class GraphCanvas():
    def __init__(self):
        pass

    def create_from_networkx(self):
        pass

    def create_from_md(self,file):
        with open(file,'r') as f:
            text = f.read()

        data = json.loads(text)

        for i in data['nodes']:
            del i["y"],i["x"],i["width"],i["type"],i["styleAttributes"],i["height"]    

        
        # 初始化 Mermaid 代码字符串
        mermaid_code = "graph TD\n"

        # 添加节点
        for node in data['nodes']:
            node_id = node['id']
            node_text = node['text'].replace('"', '\\"')  # 处理文本中的双引号
            mermaid_code += f'    {node_id}["{node_text}"]\n'

        # 添加边
        for edge in data['edges']:
            from_node = edge['fromNode']
            to_node = edge['toNode']
            mermaid_code += f'    {from_node} --> {to_node}\n'

        return mermaid_code

        pass

    def export_to_md(self):
        pass

    def export_to_networkx(self):
        pass






## #########
class GraphFiles():
    def __init__(self):
        pass

    def create_from_networkx(self):
        pass

    def create_from_files(self):
        pass

    def export_to_files(self):
        pass

    def export_to_networkx(self):
        pass

class GraphMermaid():
    def __init__(self):
        pass

    def create_from_networkx(self):
        pass

    def create_from_md(self):
        pass

    def export_to_md(self):
        pass

    def export_to_networkx(self):
        pass


class GraphNeo4j():
    def __init__(self):
        pass

    def create_from_networkx(self):
        pass

    def create_from_md(self):
        pass

    def export_to_md(self):
        pass

    def export_to_networkx(self):
        pass
