# # 暴力编写 + AI优化 将垃圾代码转化为牛逼代码
import re
def work(text:str):
    # 正则表达式匹配 title 属性
    match = re.search(r'\[\[(.*?)\]\(', text)
    # 替换为新的 title
    new_text = re.sub(r'\[\[(.*?)\)\]', f'[{match.group(1)}]', text)
    return new_text

# where

import re
def work2(text:str):
    # 正则表达式匹配 title 属性
    match = re.search(r'!\[\[(.*?)\]', text)
    # 替换为新的 title
    new_text = re.sub(r'!\[\[(.*?)\]\]', f'{match.group(1)}', text)
    return new_text

def convert_to_mermaid(data):
    nodes = data['nodes']
    edges = data['edges']

    # 处理节点
    node_lines = []
    for node in nodes:
        node_id = node['id']
        node_text = node.get('text') or node.get('file')
        node_lines.append(f"{node_id}[{node_text}]")

    # 处理边
    edge_lines = []
    for edge in edges:
        from_node = edge['fromNode']
        to_node = edge['toNode']
        if 'label' in edge:
            label = edge['label']
            edge_lines.append(f"{from_node} -->|{label}| {to_node}")
        else:
            edge_lines.append(f"{from_node} --> {to_node}")
        
    node_lines2 = []
    for node in node_lines:
        try:
            node = work(node)
        except:
            pass
        try:
            node = work2(node)
        except:
            pass
        node_lines2.append(node)
        
    
    # 生成 Mermaid.js 格式
    mermaid_graph = "graph TD\n   "
    mermaid_graph += "\n   ".join(node_lines2) + "\n   "
    mermaid_graph += "\n   ".join(edge_lines)

    return mermaid_graph


if __name__ == "__main__":


    # 调用函数
    mermaid_graph = convert_to_mermaid(dict_1)
    print(mermaid_graph)