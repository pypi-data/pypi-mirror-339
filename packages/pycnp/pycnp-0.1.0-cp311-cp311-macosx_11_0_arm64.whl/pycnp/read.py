"""
read.py - 图数据文件读取工具模块

提供读取不同格式的图文件（邻接表或边列表）和权重文件的功能，
将读取的数据转换为PyCNP的ProblemData对象
"""

import os
from typing import Optional
import PyCNP


def read(graph_file: str, weight_file: Optional[str] = None) -> 'PyCNP.ProblemData':
    """
    读取图文件和权重文件，返回ProblemData对象
    
    自动检测图文件格式（邻接表或边列表），并读取相应的数据。
    如果提供了权重文件，则同时读取节点权重。
    
    参数:
        graph_file: 图文件路径（邻接表或边列表格式）
        weight_file: 权重文件路径（可选）
        
    返回:
        PyCNP.ProblemData 对象
        
    异常:
        RuntimeError: 当文件无法打开或格式错误时抛出
        FileNotFoundError: 当文件不存在时抛出
    """
    if not os.path.exists(graph_file):
        raise FileNotFoundError(f"找不到图文件: {graph_file}")
    
    # 确定文件格式（邻接表或边列表）
    with open(graph_file, 'r', encoding='utf-8') as f:
        first_line = f.readline().strip()
        
        # 检查第一行是否包含 'p' 字符，这是边列表格式的特征
        if first_line.startswith('p') or 'p' in first_line.split():
            # 边列表格式
            problem_data = read_edge_list_format(graph_file)
        else:
            # 邻接表格式
            problem_data = read_adjacency_list_format(graph_file)
    
    # 如果提供了权重文件，读取节点权重
    if weight_file and os.path.exists(weight_file):
        try:
            problem_data.read_node_weights_from_file(weight_file)
        except Exception as e:
            raise RuntimeError(f"读取权重文件失败: {e}")
    
    return problem_data


def read_adjacency_list_format(filename: str) -> 'PyCNP.ProblemData':
    """
    从邻接表格式文件读取数据
    
    邻接表格式：每行表示一个节点及其邻居，格式为"节点ID 邻居1 邻居2 ..."
    
    参数:
        filename: 文件路径
        
    返回:
        初始化的ProblemData对象
        
    异常:
        RuntimeError: 当文件无法打开或格式错误时抛出
    """
    try:
        # 调用C++绑定函数读取邻接表文件
        return PyCNP.ProblemData.read_from_adjacency_list_file(filename)
    except Exception as e:
        raise RuntimeError(f"读取邻接表文件失败: {e}")
    

def read_edge_list_format(filename: str) -> 'PyCNP.ProblemData':
    """
    从边列表格式文件读取数据
    
    边列表格式：通常包含一个头部行"p edge 节点数 边数"，
    然后每行表示一条边，格式为"e 节点1 节点2"
    
    参数:
        filename: 文件路径
        
    返回:
        初始化的ProblemData对象
        
    异常:
        RuntimeError: 当文件无法打开或格式错误时抛出
    """
    try:
        # 调用C++绑定函数读取边列表文件
        return PyCNP.ProblemData.read_from_edge_list_format(filename)
    except Exception as e:
        raise RuntimeError(f"读取边列表文件失败: {e}")


def get_node_weight(problem_data: 'PyCNP.ProblemData', node: int) -> float:
    """
    获取指定节点的权重
    
    参数:
        problem_data: ProblemData对象
        node: 节点ID
        
    返回:
        节点权重，如果节点不存在则返回-1
    """
    try:
        return problem_data.get_node_weight(node)
    except Exception as e:
        return -1.0 