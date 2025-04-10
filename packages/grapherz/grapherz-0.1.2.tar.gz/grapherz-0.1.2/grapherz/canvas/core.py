from box import Box
import json
from enum import Enum

class Color(Enum):
    gray = "0"
    red = "1"
    origne = "2"
    yellow = "3"
    green = "4"
    blue = "5"
    purpol = "6"

class Canvas():
    def __init__(self,file_path:str=None):
        """
        初始化

        file_path : str 传入格式为canvas的文件路径
        """
        self.file_path = file_path
        with open(file_path,'r') as f:
            text = f.read()
        bdict = Box(json.loads(text))
        self.bdict = bdict
        
        for edge in bdict.edges:
            if not edge.get('color'):
                edge.setdefault('color','0')
        for node in bdict.nodes:
            if not node.get('color'):
                node.setdefault('color','0')
                
        self.edges = bdict.edges
        self.nodes = bdict.nodes
    
    def add(self):
        pass
    
    def delete(self):
        pass

    
    def select_by_id(self,type:str ='edge',key:str='')->Box:
        """
        通过id 来选择 Box
        type: str edge, node
        key: str id 
        """
        def check_id(obj,id=''):
            if obj.id == id:
                return obj
        id = key
        if type == 'edge':
            for edge in self.edges:
                if check_id(edge,id=id):
                    return edge
        else:
            for node in self.nodes:
                if check_id(node,id=id):
                    return node
                
    def select_by_color(self, key: Color = '', type='edge'):
        """
        Select objects based on color.

        key: Color
            The color to filter the objects by.
        
        type: str
            The type of objects to filter ('edge', 'node', 'all').
            If 'edge', filter from edges.
            If 'node', filter from nodes.
            If 'all', filter from both nodes and edges.
            Defaults to 'edge'.
        """
        def check_key(obj, key=''):
            # Check if the object's color matches the key color
            if obj.color == key.value:
                return obj
            
        color = key
        if type == 'edge':              
            # If type is 'edge', select from edges
            objs = self.edges
        elif type == 'node':
            # If type is 'node', select from nodes
            objs = self.nodes
        elif type == 'all':
            # If type is 'all', select from both nodes and edges
            objs = self.nodes + self.edges
        else:
            # Default to select from both nodes and edges if type is unknown
            objs = self.nodes + self.edges
            
        # Return a list of objects whose color matches the key
        return [i for i in objs if check_key(i, key=color)]
    def select_nodes_by_type(self,key:str='')->list:
        """
        Select nodes based on their type.

        key: str
            The type of nodes to select. Defaults to 'text'.
        
        Returns a list of nodes with matching type.
        """
        def check_key(obj,key='text'):
            if obj.type == key:
                return obj
        objs = self.nodes
        return [i for i in objs if check_key(i,key=key)]

    def select_nodes_by_text(self,key:str='')->list:
        """
        Select nodes containing specific text.

        key: str
            The text to search for in nodes.
        
        Returns a list of nodes whose text contains the specified key.
        """
        def check_key(obj,key:str=''):
            obj_text = obj.get('text') or ''
            if key in obj_text:
                return obj
        objs = self.nodes
        return [i for i in objs if check_key(i,key=key)]
    def select_edges_by_text(self,key:str='')->list:
        """
        Select edges containing specific text.

        key: str
            The text to search for in edges.

        Returns a list of edges whose labels contain the specified key.
        """
        def check_key(obj,key:str=''):
            obj_text = obj.get('label') or ''
            if key in obj_text:
                return obj
        objs = self.edges
        return [i for i in objs if check_key(i,key=key)]
        
    def select_by_styleAttributes(self,type = 'file',key:Color=''):
        """
        Placeholder for selecting objects by style attributes.

        type: str
            The object type to select ('file', etc.).
        
        key: Color
            The color key for selection.
            
        This method is currently not implemented.
        """
        pass
    
    def to_file(self,file_path):
        """
        Write the canvas data to a specified file path in JSON format.

        file_path: str
            The path to the file where data will be written.
        """
        with open(file_path,'w') as f:
            f.write(self.bdict.to_json())

    
if __name__ == "__main__":
    canva = Canvas(file_path='/Users/zhaoxuefeng/GitHub/obsidian/工作/实验室/模拟资质认证.canvas')
    canva.select_edges_by_text(key='处理')
    canva.select_by_color(key=Color.yellow,type='node')[4].color = Color.green.value
    canva.to_file(file_path='/Users/zhaoxuefeng/GitHub/obsidian/工作/实验室/模拟资质认证.canvas')