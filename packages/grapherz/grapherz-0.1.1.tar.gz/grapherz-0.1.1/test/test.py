import sys
import os
# 将项目根目录添加到 Python 路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import re
import pytest
from grapher.adapter import CanvasAdapter,FilesAdapter,MermaidAdapter,Neo4jAdapter
# 测试CanvasAdapter
def test_canvas_adapter():
    canvas = CanvasAdapter()
    
    # 测试pull方法
    data = canvas.pull()
    assert "canvas_data" in data
    assert data["canvas_data"] == "图表数据"
    
    # 测试to_networkx方法
    networkx_data = canvas.to_networkx(data)
    assert "networkx_data" in networkx_data
    assert networkx_data["networkx_data"] == "转换后的数据"
    
    # 测试from_networkx方法
    converted_data = canvas.from_networkx(networkx_data)
    assert "canvas_data" in converted_data
    assert converted_data["canvas_data"] == "转换后的数据"
    
    # 测试push方法
    canvas.push(converted_data)

# 测试FilesAdapter
def test_files_adapter():
    files = FilesAdapter()
    
    # 测试pull方法
    data = files.pull()
    assert "file_data" in data
    assert data["file_data"] == "文件数据"
    
    # 测试to_networkx方法
    networkx_data = files.to_networkx(data)
    assert "networkx_data" in networkx_data
    assert networkx_data["networkx_data"] == "转换后的数据"
    
    # 测试from_networkx方法
    converted_data = files.from_networkx(networkx_data)
    assert "file_data" in converted_data
    assert converted_data["file_data"] == "转换后的数据"
    
    # 测试push方法
    files.push(converted_data)

# 测试MermaidAdapter
def test_mermaid_adapter():
    mermaid = MermaidAdapter()
    
    # 测试pull方法
    data = mermaid.pull()
    assert "mermaid_data" in data
    assert data["mermaid_data"] == "Mermaid图表数据"
    
    # 测试to_networkx方法
    networkx_data = mermaid.to_networkx(data)
    assert "networkx_data" in networkx_data
    assert networkx_data["networkx_data"] == "转换后的数据"
    
    # 测试from_networkx方法
    converted_data = mermaid.from_networkx(networkx_data)
    assert "mermaid_data" in converted_data
    assert converted_data["mermaid_data"] == "转换后的数据"
    
    # 测试push方法
    mermaid.push(converted_data)

# 测试Neo4jAdapter
def test_neo4j_adapter():
    neo4j = Neo4jAdapter()
    
    # 测试pull方法
    data = neo4j.pull()
    assert "neo4j_data" in data
    assert data["neo4j_data"] == "图数据库数据"
    
    # 测试to_networkx方法
    networkx_data = neo4j.to_networkx(data)
    assert "networkx_data" in networkx_data
    assert networkx_data["networkx_data"] == "转换后的数据"
    
    # 测试from_networkx方法
    converted_data = neo4j.from_networkx(networkx_data)
    assert "neo4j_data" in converted_data
    assert converted_data["neo4j_data"] == "转换后的数据"
    
    # 测试push方法
    neo4j.push(converted_data)

# 测试数据流动
def test_data_flow():
    canvas = CanvasAdapter()
    files = FilesAdapter()
    mermaid = MermaidAdapter()
    neo4j = Neo4jAdapter()
    
    # 从Canvas拉取数据，转换并推送到Files
    canvas_data = canvas.pull()
    networkx_data = canvas.to_networkx(canvas_data)
    files.push(canvas.from_networkx(networkx_data))
    
    # 从Files拉取数据，转换并推送到Mermaid
    files_data = files.pull()
    networkx_data = files.to_networkx(files_data)
    mermaid.push(files.from_networkx(networkx_data))
    
    # 从Mermaid拉取数据，转换并推送到Neo4j
    mermaid_data = mermaid.pull()
    networkx_data = mermaid.to_networkx(mermaid_data)
    neo4j.push(mermaid.from_networkx(networkx_data))
    
    # 从Neo4j拉取数据，转换并推送到Canvas
    neo4j_data = neo4j.pull()
    networkx_data = neo4j.to_networkx(neo4j_data)
    canvas.push(neo4j.from_networkx(networkx_data))