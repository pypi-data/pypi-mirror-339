import sys
import os
# 将项目根目录添加到 Python 路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import re
import pytest


from grapherz.canvas.core import Canvas, Color



def test_canvas():
    canva = Canvas(file_path='/Users/zhaoxuefeng/GitHub/obsidian/工作/实验室/模拟资质认证.canvas')
    canva.select_edges_by_text(key='处理')
    canva.select_by_color(key=Color.yellow,type='node')[4].color = Color.green.value
    canva.to_file(file_path='/Users/zhaoxuefeng/GitHub/obsidian/工作/实验室/模拟资质认证.canvas')




