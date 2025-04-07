"""
Model.py - 图问题的建模和求解类

提供了创建图模型、添加节点和边、调用求解算法的统一接口
"""

from typing import Set, Dict, List, Optional, Union, Any, Tuple
import PyCNP
from pycnp.stop import StoppingCriterion, MaxIterations, MaxRuntime, NoImprovement
from pycnp.MemeticSearch import MemeticSearch, MemeticSearchParams
from pycnp.Result import Result


class Model:
    """
    图问题的建模和求解类
    
    整合了不同类型图的创建、配置和调用各种求解算法的功能。
    提供了构建图模型、配置求解参数和执行求解的统一接口。
    """
    
    def __init__(self):
        """
        初始化图模型
        
        创建一个空的图模型，包含节点、边和节点权重的数据结构
        """
        self.nodes = set()         # 节点集合
        self.adj_list = []         # 邻接表
        self.node_weights = {}     # 节点权重字典
        self.stopping_criterion = None  # 停止准则
    
    def add_node(self, node: int) -> None:
        """
        添加节点到模型
        
        参数:
            node: 要添加的节点ID
            
        注意:
            如果节点已存在，则不会重复添加
        """
        self.nodes.add(node)
        
        # 如果节点不在权重字典中，则添加默认权重
        if node not in self.node_weights:
            self.node_weights[node] = 0.0
        
        # 调整邻接表大小
        while len(self.adj_list) <= node:
            self.adj_list.append(set())
    
    def add_node_weight(self, node: int, weight: float) -> None:
        """
        设置节点权重
        
        参数:
            node: 节点ID
            weight: 节点权重
            
        注意:
            如果节点不存在，会自动添加该节点
        """
        # 确保节点存在
        if node not in self.nodes:
            self.add_node(node)
            
        self.node_weights[node] = weight
    
    def add_edge(self, u: int, v: int) -> None:
        """
        添加边到模型
        
        参数:
            u: 边的第一个端点
            v: 边的第二个端点
            
        注意:
            如果节点不存在，会自动添加节点
        """
        # 确保节点存在
        if u not in self.nodes:
            self.add_node(u)
        if v not in self.nodes:
            self.add_node(v)
            
        # 确保邻接表足够大
        while len(self.adj_list) <= max(u, v):
            self.adj_list.append(set())
        
        # 添加边（无向图添加两个方向）
        self.adj_list[u].add(v)
        self.adj_list[v].add(u)
    
    def set_stopping_criterion(self, criterion: StoppingCriterion) -> None:
        """
        设置停止准则
        
        参数:
            criterion: 停止准则对象，必须实现StoppingCriterion协议
        """
        self.stopping_criterion = criterion
    
    def get_node_count(self) -> int:
        """
        获取图中的节点数量
        
        返回:
            图中的节点数量
        """
        return len(self.nodes)
    
    def get_edge_count(self) -> int:
        """
        获取图中的边数量
        
        返回:
            图中的边数量
        """
        # 计算总边数（除以2因为无向图中每条边被计算了两次）
        return sum(len(neighbors) for neighbors in self.adj_list) // 2
    
    @staticmethod
    def from_data(problem_data: 'PyCNP.ProblemData') -> 'Model':
        """
        从问题数据创建模型的静态工厂方法
        
        参数:
            problem_data: PyCNP.ProblemData问题数据对象
            
        返回:
            初始化好的模型实例
        """
        model = Model()
        
        # 保存问题数据引用，以便在solve方法中使用
        model._problem_data = problem_data
        
        return model
    
    def _create_problem_data(self) -> 'PyCNP.ProblemData':
        """
        创建ProblemData对象
        
        将模型数据转换为PyCNP的ProblemData对象
        
        返回:
            初始化的ProblemData对象
        """
        # 创建新的ProblemData对象
        max_node_id = max(self.nodes) if self.nodes else 0
        problem_data = PyCNP.ProblemData(max_node_id + 1)
        
        # 添加节点
        for node in self.nodes:
            problem_data.add_node(node)
        
        # 添加节点权重    
        for node, weight in self.node_weights.items():
            problem_data.add_node_weight(node, weight)
        
        # 添加边（避免重复添加）
        for u in range(len(self.adj_list)):
            for v in self.adj_list[u]:
                if u < v:  # 只添加一次无向边
                    problem_data.add_edge(u, v)
        
        return problem_data
    
    def solve(self, 
              problem_type: str, 
              bound: int, 
              K: int = 2**30,
              memetic_search_params: Optional[MemeticSearchParams] = None, 
              is_ir_used: bool = True, 
              seed: int = 0,
              stopping_criterion: Optional[StoppingCriterion] = None,
              verbose: bool = False) -> 'Result':
        """
        解决模型定义的图问题
        
        参数:
            problem_type: 问题类型 ("CNP", "DCNP", "NWCNP")
            bound: 需要移除的节点数量
            K: NWCNP问题的k值(默认无穷大，用系统最大整数表示)
            memetic_search_params: 种群算法参数
            is_ir_used: 是否使用IR技术
            seed: 随机数种子
            stopping_criterion: 停止准则
            verbose: 是否输出详细信息
            
        返回:
            求解结果，包含最优解和目标值
            
        异常:
            RuntimeError: 当问题类型未知或未设置停止准则时
        """
        # 使用传入的停止准则或已设置的停止准则
        criterion = stopping_criterion or self.stopping_criterion
        if criterion is None:
            raise RuntimeError("未设置停止准则，请使用set_stopping_criterion方法设置或在solve中提供")
        
        # 设置默认参数
        if memetic_search_params is None:
            memetic_search_params = MemeticSearchParams()
        
        # 获取或创建问题数据
        if hasattr(self, '_problem_data'):
            # 使用已有的problem_data
            problem_data = self._problem_data
        else:
            # 从模型数据创建新的ProblemData对象
            problem_data = self._create_problem_data()
        
        # 创建MemeticSearch并执行
        try:
            ms = MemeticSearch(
                problem_data=problem_data,
                problem_type=problem_type,
                bound=bound,
                K=K,
                memetic_search_params=memetic_search_params,
                is_ir_used=is_ir_used,
                seed=seed,
                stopping_criterion=criterion,
                verbose=verbose
            )
            
            # 运行算法获取结果
            result = ms.run()
            return result
        except Exception as e:
            raise RuntimeError(f"求解过程中发生错误: {e}")
    
    def __str__(self) -> str:
        """
        返回图模型的字符串表示
        
        返回:
            描述图模型的字符串，包含节点数和边数
        """
        return f"Model(节点数: {self.get_node_count()}, 边数: {self.get_edge_count()})"
    
    def __repr__(self) -> str:
        """
        返回图模型的详细字符串表示
        
        返回:
            详细描述图模型的字符串
        """
        return f"Model(节点: {sorted(list(self.nodes))}, 边数: {self.get_edge_count()})"
