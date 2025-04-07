"""
PyCNP - Python绑定的CNP求解器包

提供了解决图临界节点问题(Critical Node Problem)的各种算法和数据结构
"""

from typing import Set, Dict, Any, Optional

# 导入C++绑定的PyCNP模块
from PyCNP import (
    # 常量
    CNP, DCNP, NWCNP,      # 问题类型
    CBNS, CHNS, DLAS, BCLS, # 搜索策略
    
    # 类
    ProblemData
)

# 导入Python实现的停止准则
from pycnp.stop import (
    StoppingCriterion,
    MaxIterations,
    MaxRuntime,
    NoImprovement,
    MultipleCriteria
)

# 导入Python实现的MemeticSearch和参数类
from .MemeticSearch import (
    MemeticSearch, 
    MemeticSearchParams,
)

# 导入Python实现的Model类
from .Model import Model 

# 导入读取函数
from .read import read, get_node_weight

# 导入Result类
from .Result import Result

# 版本信息
__version__ = "0.1.0"

__all__ = [
    # C++绑定常量
    'CNP', 'DCNP', 'NWCNP',  # 问题类型
    'CBNS', 'CHNS', 'DLAS', 'BCLS',  # 搜索策略
    
    # C++绑定类
    'ProblemData',
    
    # 停止准则
    'StoppingCriterion', 'MaxIterations', 'MaxRuntime', 'NoImprovement', 'MultipleCriteria',
    
    # 种群搜索
    'MemeticSearch', 'MemeticSearchParams',
    
    # 模型类
    'Model',
    
    # 结果类
    'Result',
    
    # 工具函数
    'read', 'get_node_weight',
] 